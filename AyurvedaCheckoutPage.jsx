
import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { CreditCard, ShieldCheck, Truck, ShoppingBag, ArrowLeft, Plus, MapPin, User, Phone, Mail, Home } from 'lucide-react';
import { motion } from 'framer-motion';
import ScrollRevealSection from '@/components/common/ScrollRevealSection';
import AnimatedTextWord from '@/components/common/AnimatedTextWord';
import { useCart } from '@/contexts/CartContext';
import { useAuth } from '@/contexts/AuthContext';
import apiService from '@/services/api';

const loadRazorpayScript = () => {
  return new Promise((resolve, reject) => {
    if (window.Razorpay) {
      console.log('Razorpay script already loaded');
      return resolve(true);
    }

    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;

    const timeout = setTimeout(() => {
      reject(new Error('Razorpay script loading timed out after 10 seconds'));
    }, 10000);

    script.onload = () => {
      clearTimeout(timeout);
      console.log('Razorpay script loaded successfully');
      resolve(true);
    };

    script.onerror = () => {
      clearTimeout(timeout);
      console.error('Failed to load Razorpay script from https://checkout.razorpay.com/v1/checkout.js');
      reject(new Error('Failed to load Razorpay checkout script. Please check your network or try again later.'));
    };

    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  });
};

const AyurvedaCheckoutPage = () => {
  const { cart, clearCart } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [profileLoading, setProfileLoading] = useState(false);
  const [customerProfile, setCustomerProfile] = useState(null);
  const [customerAddresses, setCustomerAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [showAddAddress, setShowAddAddress] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    phone: '',
    address: '',
    apartment: '',
    city: '',
    country: 'IN',
    state: '',
    zipCode: '',
    paymentMethod: 'cod',
  });
  const [newAddress, setNewAddress] = useState({
    address: '',
    apartment: '',
    city: '',
    state: '',
    zipCode: '',
    mobile: '',
    isDefault: false,
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [razorpayLoading, setRazorpayLoading] = useState(false);
  const [paymentError, setPaymentError] = useState('');
  const razorpayOrderIdRef = useRef(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: '/checkout' } } });
      return;
    }
    fetchCustomerData();

    return () => {
      const script = document.querySelector('script[src="https://checkout.razorpay.com/v1/checkout.js"]');
      if (script && document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, [isAuthenticated, navigate]);

  const fetchCustomerData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getCustomerProfile();
      if (response?.success && response?.data) {
        const profileData = response.data;
        setCustomerProfile(profileData);

        const addressesData = [
          ...(profileData.addresses || []).map(addr => ({
            ...addr,
            zip_code: addr.zip_code || addr.pincode || '',
            is_default: addr.is_default || false,
          })),
          ...(profileData.more_addresses || []).map(addr => ({
            ...addr,
            zip_code: addr.zip_code || addr.pincode || '',
            is_default: false,
          })),
        ];
        setCustomerAddresses(addressesData);

        if (profileData) {
          setFormData(prev => ({
            ...prev,
            email: profileData.email || '',
            firstName: profileData.name ? profileData.name.split(' ')[0] : '',
            lastName: profileData.name ? profileData.name.split(' ').slice(1).join(' ') : '',
            phone: profileData.mobiles && profileData.mobiles.length > 0 ? profileData.mobiles[0].mobile : '',
          }));
        }

        if (addressesData.length > 0) {
          const defaultAddress = addressesData.find(addr => addr.is_default) || addressesData[0];
          setSelectedAddress(defaultAddress);
          setFormData(prev => ({
            ...prev,
            address: defaultAddress.address || '',
            apartment: defaultAddress.apartment || '',
            city: defaultAddress.city || '',
            state: defaultAddress.state || '',
            zipCode: defaultAddress.zip_code || '',
          }));
        }
      } else {
        throw new Error('Invalid API response structure');
      }
    } catch (error) {
      console.error('Error fetching customer data:', error);
      setPaymentError('Failed to load customer data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const updatedFormData = { ...prev, [name]: value };
      localStorage.setItem('checkout_form_data', JSON.stringify(updatedFormData));
      return updatedFormData;
    });
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAddressSelect = (address) => {
    setSelectedAddress(address);
    setFormData(prev => ({
      ...prev,
      address: address.address || '',
      apartment: address.apartment || '',
      city: address.city || '',
      state: address.state || '',
      zipCode: address.zip_code || '',
    }));
  };

  const handleNewAddressChange = (e) => {
    const { name, value } = e.target;
    setNewAddress(prev => ({ ...prev, [name]: value }));
  };

  const handleAddAddress = async () => {
    try {
      setProfileLoading(true);
      if (!newAddress.address || !newAddress.city || !newAddress.state || !newAddress.zipCode) {
        alert('Please fill in all required address fields (Address, City, State, ZIP Code)');
        return;
      }

      const addressData = {
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        mobile: newAddress.mobile || formData.phone,
        email: formData.email,
        address: newAddress.address,
        apartment: newAddress.apartment,
        pincode: newAddress.zipCode,
        city: newAddress.city,
        state: newAddress.state,
        country: 'IN',
      };

      const existingAddresses = customerAddresses.filter(addr => addr.zip_code);
      const updatedMoreAddresses = [...(customerProfile?.more_addresses || []), addressData];

      const profileUpdateData = {
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        email: formData.email,
        mobile: formData.phone,
        addresses: existingAddresses,
        more_addresses: updatedMoreAddresses,
      };

      await apiService.updateCustomerProfile(profileUpdateData);
      setCustomerAddresses([...existingAddresses, ...updatedMoreAddresses.map(addr => ({
        ...addr,
        zip_code: addr.pincode,
      }))]);
      setShowAddAddress(false);
      setNewAddress({
        address: '',
        apartment: '',
        city: '',
        state: '',
        zipCode: '',
        mobile: '',
        isDefault: false,
      });
      await fetchCustomerData();
      alert('Address added successfully!');
    } catch (error) {
      console.error('Error adding address:', error);
      alert('Failed to add address. Please try again.');
    } finally {
      setProfileLoading(false);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      setProfileLoading(true);
      if (!formData.firstName || !formData.lastName || !formData.email || !formData.phone) {
        alert('Please fill in all required fields (First Name, Last Name, Email, Phone)');
        return;
      }

      const existingAddresses = (customerProfile?.addresses || []).map(addr => ({
        ...addr,
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        mobile: addr.mobile || formData.phone,
        email: formData.email,
        pincode: addr.zip_code || addr.pincode,
        country: addr.country || 'IN',
      })).filter(addr => addr.pincode);

      const moreAddresses = (customerProfile?.more_addresses || []).map(addr => ({
        ...addr,
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        mobile: addr.mobile || formData.phone,
        email: formData.email,
        pincode: addr.zip_code || addr.pincode,
        country: addr.country || 'IN',
      })).filter(addr => addr.pincode);

      const profileData = {
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        email: formData.email,
        mobile: formData.phone,
        addresses: existingAddresses,
        more_addresses: moreAddresses,
      };

      await apiService.updateCustomerProfile(profileData);
      await fetchCustomerData();
      alert('Profile updated successfully!');
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile. Please try again.');
    } finally {
      setProfileLoading(false);
    }
  };

  const createRazorpayOrder = async (amount) => {
    try {
      if (!amount || isNaN(amount) || amount <= 0) {
        throw new Error('Invalid order amount');
      }

      // Fix: Use the correct API endpoint directly
      const response = await fetch('/api/dashboard/rz/orderid/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Add auth if needed
        },
        body: JSON.stringify({
          amount: Number(amount).toFixed(2), // Send amount in rupees
          currency: 'INR',
          receipt: `order_${Date.now()}`,
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create order');
      }

      const data = await response.json();
      
      if (!data.success || !data.order_id) {
        throw new Error('Invalid Razorpay order response');
      }
      
      console.log('Razorpay order response:', data);
      return {
        id: data.order_id,
        amount: data.amount, // This will be in paise from backend
        currency: data.currency,
        key_id: data.key_id, // Use key_id from backend response
      };
    } catch (error) {
      console.error('Error creating Razorpay order:', error);
      throw error;
    }
  };

  const handleRazorpayPayment = async (order) => {
    try {
      console.log('Starting Razorpay payment with order:', order);
      const res = await loadRazorpayScript();
      if (!res) {
        throw new Error('Failed to load Razorpay SDK. Please check your network connection or try again later.');
      }

      if (!window.Razorpay) {
        throw new Error('Razorpay SDK not available after loading. Please try again.');
      }

      if (!order.id || !order.amount || !order.currency || !order.key_id) {
        throw new Error('Invalid Razorpay order data. Missing required fields.');
      }

      const options = {
        key: order.key_id, // Use key_id from backend response
        amount: order.amount, // This should be in paise
        currency: order.currency,
        name: 'Kushnath Ayurveda',
        description: 'Order Payment',
        order_id: order.id,
        handler: async function (response) {
          try {
            console.log('Payment success response:', response);
            
            // Verify payment with your backend
            const verifyResponse = await fetch('/api/dashboard/rz/verify-payment/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
              },
              body: JSON.stringify({
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_signature: response.razorpay_signature,
              })
            });

            if (verifyResponse.ok) {
              alert(`Payment successful! Payment ID: ${response.razorpay_payment_id}`);
              clearCart();
              navigate('/orders');
            } else {
              throw new Error('Payment verification failed');
            }
          } catch (error) {
            console.error('Payment verification error:', error);
            setPaymentError('Payment verification failed. Please contact support.');
            setIsProcessing(false);
          }
        },
        prefill: {
          name: `${formData.firstName} ${formData.lastName}`.trim(),
          email: formData.email,
          contact: formData.phone,
        },
        theme: {
          color: '#0E9F6E',
        },
        modal: {
          ondismiss: () => {
            console.log('Razorpay modal dismissed by user');
            setIsProcessing(false);
          },
        },
        notes: {
          attempt: 'checkout_attempt_' + Date.now(),
        },
        // Force test mode configuration
        config: {
          display: {
            blocks: {
              utib: {
                name: "Pay using UPI",
                instruments: [
                  {
                    method: "upi"
                  }
                ]
              }
            },
            sequence: ["block.utib"],
            preferences: {
              show_default_blocks: false
            }
          }
        }
      };
      console.log('Razorpay options:', options);

      const rzp = new window.Razorpay(options);
      
      // Add event listeners
      rzp.on('payment.failed', (response) => {
        console.error('Payment failed:', response.error);
        setPaymentError(`Payment failed: ${response.error.description}`);
        setIsProcessing(false);
      });

      rzp.on('payment.cancelled', () => {
        console.log('Payment cancelled by user');
        setPaymentError('Payment was cancelled');
        setIsProcessing(false);
      });

      console.log('Opening Razorpay modal');
      try {
        rzp.open();
        console.log('Razorpay modal opened successfully');
      } catch (openError) {
        console.error('Error opening Razorpay modal:', openError);
        if (openError.message && openError.message.includes('blocked')) {
          throw new Error('Razorpay payment window was blocked. Please disable popup blockers for this site and try again.');
        } else if (openError.message && openError.message.includes('refused')) {
          throw new Error('Razorpay connection refused. Please check your network or contact support.');
        }
        throw new Error('Failed to open Razorpay payment window. Please check your network or contact support.');
      }
    } catch (error) {
      console.error('Razorpay payment error:', error);
      setPaymentError(error.message || 'Failed to initiate payment. Please try Cash on Delivery or contact support.');
      setIsProcessing(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setPaymentError('');

    const cartItems = cart.items || [];
    if (cartItems.length === 0) {
      alert('Your cart is empty. Please add items to proceed.');
      return;
    }

    if (!selectedAddress) {
      alert('Please select a delivery address');
      return;
    }

    const hasZipCode = selectedAddress.zip_code || selectedAddress.pincode;
    const hasAddress = selectedAddress.address;
    const hasCity = selectedAddress.city;
    const hasState = selectedAddress.state;

    const missingFields = [];
    if (!hasAddress) missingFields.push('Address');
    if (!hasCity) missingFields.push('City');
    if (!hasState) missingFields.push('State');
    if (!hasZipCode) missingFields.push('ZIP Code');

    if (missingFields.length > 0) {
      alert(`Please complete the delivery address. Missing: ${missingFields.join(', ')}`);
      return;
    }

    if (!finalTotal || isNaN(finalTotal) || finalTotal <= 0) {
      console.log('Cart data:', cart);
      console.log('Subtotal:', subtotal, 'DiscountedTotal:', discountedTotal, 'FinalTotal:', finalTotal);
      setPaymentError('Invalid cart total. Please check your cart and try again.');
      return;
    }

    setIsProcessing(true);

    try {
      if (formData.paymentMethod === 'razorpay') {
        setRazorpayLoading(true);
        const order = await createRazorpayOrder(finalTotal);
        razorpayOrderIdRef.current = order.id;
        setRazorpayLoading(false);
        await handleRazorpayPayment(order);
        return;
      }

      const loginPhoneNumber = localStorage.getItem('login_phone_number');
      const orderData = {
        customer_mobile: loginPhoneNumber || formData.phone,
        payment_method: formData.paymentMethod,
        recipient_name: `${formData.firstName} ${formData.lastName}`.trim(),
        recipient_phone: formData.phone,
        notes: formData.notes || '',
        delivery_pincode: selectedAddress.zip_code || selectedAddress.pincode,
        delivery_city: selectedAddress.city,
        delivery_state: selectedAddress.state,
        delivery_country: selectedAddress.country || 'India',
        delivery_address_text: selectedAddress.address,
        order_items: cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
        })),
      };

      const orderResponse = await apiService.createOrder(orderData);
      if (orderResponse?.id || orderResponse?.order_id) {
        clearCart();
        const orderId = orderResponse.order_id || orderResponse.id;
        alert(`Order placed successfully! Order ID: ${orderId}`);
        navigate('/orders');
      } else {
        throw new Error('Order creation failed - no order ID received');
      }
    } catch (error) {
      console.error('Order submission error:', error);
      setPaymentError(error.message || 'Failed to place order. Please try again.');
    } finally {
      setIsProcessing(false);
      setRazorpayLoading(false);
    }
  };

  const cartItems = cart.items || [];
  const totals = cart.totals || {};
  const subtotal = Number(totals.subtotal) || 0;
  const discountedTotal = Number(totals.total) || 0;
  const totalSavings = Number(totals.totalSavings) || 0;
  const shippingCost = discountedTotal > 50 ? 0 : 7.99;
  const finalTotal = discountedTotal + shippingCost;

  const FormField = ({ id, name, label, type = "text", placeholder, value, onChange, children, required = true }) => (
    <div className="mb-4">
      <Label htmlFor={id} className="block text-sm font-medium text-kushnath-foreground mb-1.5">
        {label} {required && <span className="text-kushnath-destructive">*</span>}
      </Label>
      {children || (
        <Input
          type={type}
          id={id}
          name={name || id}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required={required}
          className="bg-kushnath-input border-kushnath-border focus:border-kushnath-primary focus:ring-kushnath-primary"
        />
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="bg-kushnath-background min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-kushnath-primary mx-auto mb-4"></div>
          <p className="text-kushnath-muted-foreground">Loading checkout...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-kushnath-background min-h-screen">
      <ScrollRevealSection className="bg-kushnath-secondary-background pt-12 text-center">
        <div className="container">
          <AnimatedTextWord text="Checkout" className="section-title mb-3" />
          <AnimatedTextWord text="Complete your order securely." className="section-subtitle mt-0" />
        </div>
      </ScrollRevealSection>

      <div className="container py-6 md:py-12">
        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8 md:gap-12">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="lg:col-span-2 bg-kushnath-card p-6 md:p-8 rounded-xl shadow-xl border border-kushnath-border"
          >
            <Accordion type="multiple" defaultValue={['contact-info', 'shipping-address', 'payment-method']} className="w-full">
              <AccordionItem value="contact-info" className="border-b border-kushnath-border">
                <AccordionTrigger className="py-4 text-lg font-serif font-semibold text-kushnath-foreground hover:no-underline">
                  <div className="flex items-center">
                    <User className="h-5 w-5 mr-2" />
                    Contact Information
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pt-2 pb-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                    <FormField id="firstName" label="First Name" placeholder="John" value={formData.firstName} onChange={handleInputChange} />
                    <FormField id="lastName" label="Last Name" placeholder="Doe" value={formData.lastName} onChange={handleInputChange} />
                  </div>
                  <FormField id="email" label="Email Address" type="email" placeholder="you@example.com" value={formData.email} onChange={handleInputChange} />
                  <FormField id="phone" label="Phone Number" type="tel" placeholder="+91 98765 43210" value={formData.phone} onChange={handleInputChange} />
                  <div className="flex gap-2 mt-4">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleUpdateProfile}
                      disabled={profileLoading}
                      className="flex-1"
                    >
                      {profileLoading ? 'Updating...' : 'Update Profile'}
                    </Button>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="shipping-address" className="border-b border-kushnath-border">
                <AccordionTrigger className="py-4 text-lg font-serif font-semibold text-kushnath-foreground hover:no-underline">
                  <div className="flex items-center">
                    <MapPin className="h-5 w-5 mr-2" />
                    Shipping Address
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pt-2 pb-4">
                  {customerAddresses.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-sm font-medium text-kushnath-foreground mb-3">Select Address</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-48 overflow-y-auto">
                        {customerAddresses.map((address, index) => (
                          <div
                            key={index}
                            onClick={() => handleAddressSelect(address)}
                            className={`p-3 border rounded-lg cursor-pointer transition-all ${
                              selectedAddress === address
                                ? 'border-kushnath-primary bg-kushnath-primary/5'
                                : 'border-kushnath-border hover:border-kushnath-primary/50'
                            }`}
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <p className="text-sm font-medium text-kushnath-foreground">{address.address}</p>
                                {address.apartment && <p className="text-xs text-kushnath-muted-foreground">{address.apartment}</p>}
                                <p className="text-xs text-kushnath-muted-foreground">
                                  {address.city}, {address.state} {address.zip_code}
                                </p>
                                {address.mobile && (
                                  <p className="text-xs text-kushnath-muted-foreground">
                                    📞 {address.mobile}
                                  </p>
                                )}
                              </div>
                              {address.is_default && (
                                <span className="text-xs bg-kushnath-primary text-white px-2 py-1 rounded">Default</span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {showAddAddress ? (
                    <div className="mb-6 p-4 border border-kushnath-border rounded-lg bg-kushnath-secondary/20">
                      <h4 className="text-sm font-medium text-kushnath-foreground mb-3">Add New Address</h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                        <FormField id="newAddress" name="address" label="Address" placeholder="123 Wellness St" value={newAddress.address} onChange={handleNewAddressChange} />
                        <FormField id="newApartment" name="apartment" label="Apartment (optional)" placeholder="Apt 4B" value={newAddress.apartment} onChange={handleNewAddressChange} required={false} />
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                        <FormField id="newMobile" name="mobile" label="Mobile Number" type="tel" placeholder="+91 98765 43210" value={newAddress.mobile} onChange={handleNewAddressChange} required={false} />
                        <FormField id="newZipCode" name="zipCode" label="ZIP Code" placeholder="400001" value={newAddress.zipCode} onChange={handleNewAddressChange} />
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4">
                        <FormField id="newCity" name="city" label="City" placeholder="Mumbai" value={newAddress.city} onChange={handleNewAddressChange} />
                        <FormField id="newState" name="state" label="State" placeholder="Maharashtra" value={newAddress.state} onChange={handleNewAddressChange} />
                      </div>
                      <div className="flex gap-2 mt-4">
                        <Button
                          type="button"
                          variant="outline"
                          onClick={() => setShowAddAddress(false)}
                          className="flex-1"
                        >
                          Cancel
                        </Button>
                        <Button
                          type="button"
                          onClick={handleAddAddress}
                          disabled={profileLoading}
                          className="flex-1"
                        >
                          {profileLoading ? 'Adding...' : 'Add Address'}
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setShowAddAddress(true)}
                      className="mb-4"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Add New Address
                    </Button>
                  )}

                  <div className="border-t border-kushnath-border pt-4">
                    <h4 className="text-sm font-medium text-kushnath-foreground mb-3">Or Enter Address Manually</h4>
                    <FormField id="address" label="Address" placeholder="123 Wellness St" value={formData.address} onChange={handleInputChange} />
                    <FormField id="apartment" label="Apartment, suite, etc. (optional)" placeholder="Apt 4B" value={formData.apartment} onChange={handleInputChange} required={false} />
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-x-4">
                      <FormField id="city" label="City" placeholder="Mumbai" value={formData.city} onChange={handleInputChange} />
                      <FormField id="state" label="State" placeholder="Maharashtra" value={formData.state} onChange={handleInputChange} />
                      <FormField id="zipCode" label="ZIP Code" placeholder="400001" value={formData.zipCode} onChange={handleInputChange} />
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="payment-method" className="border-b-0">
                <AccordionTrigger className="py-4 text-lg font-serif font-semibold text-kushnath-foreground hover:no-underline">
                  <div className="flex items-center">
                    <CreditCard className="h-5 w-5 mr-2" />
                    Payment Method
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pt-2 pb-4">
                  <p className="text-sm text-kushnath-muted-foreground mb-4">Choose your preferred payment method.</p>
                  <RadioGroup
                    value={formData.paymentMethod}
                    onValueChange={(value) => handleSelectChange('paymentMethod', value)}
                    className="space-y-3"
                  >
                    <div className="flex items-center space-x-2 p-3 border border-kushnath-border rounded-lg hover:bg-kushnath-secondary/20">
                      <RadioGroupItem value="cod" id="cod" />
                      <Label htmlFor="cod" className="flex items-center cursor-pointer">
                        <Truck className="h-5 w-5 mr-2 text-kushnath-primary" />
                        <div>
                          <p className="font-medium text-kushnath-foreground">Cash on Delivery</p>
                          <p className="text-xs text-kushnath-muted-foreground">Pay when you receive your order</p>
                        </div>
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2 p-3 border border-kushnath-border rounded-lg hover:bg-kushnath-secondary/20">
                      <RadioGroupItem value="razorpay" id="razorpay" />
                      <Label htmlFor="razorpay" className="flex items-center cursor-pointer">
                        <CreditCard className="h-5 w-5 mr-2 text-kushnath-primary" />
                        <div>
                          <p className="font-medium text-kushnath-foreground">Razorpay</p>
                          <p className="text-xs text-kushnath-muted-foreground">Pay securely with cards, UPI, or wallets</p>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>
                  <div className="mt-4 p-3 bg-kushnath-secondary/20 rounded-lg">
                    <div className="flex items-center">
                      <ShieldCheck className="h-5 w-5 text-kushnath-primary mr-2" />
                      <p className="text-sm text-kushnath-foreground">All transactions are secure and encrypted.</p>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: "easeOut", delay: 0.1 }}
            className="lg:col-span-1"
          >
            <div className="bg-kushnath-card p-6 md:p-8 rounded-xl shadow-xl border border-kushnath-border sticky top-28">
              <h2 className="text-xl font-serif font-semibold text-kushnath-foreground mb-6 flex items-center">
                <ShoppingBag className="h-6 w-6 text-kushnath-primary mr-2.5" /> Order Summary
              </h2>
              <div className="space-y-3 mb-6 max-h-60 overflow-y-auto pr-2">
                {cartItems.length === 0 ? (
                  <div className="text-center text-kushnath-muted-foreground py-8">Your cart is empty.</div>
                ) : (
                  cartItems.map(item => (
                    <div key={item.id} className="flex items-center justify-between gap-3 pb-3 border-b border-kushnath-border/70 last:border-b-0 last:pb-0">
                      <div className="flex items-center gap-3">
                        <div className="w-14 h-14 rounded-md overflow-hidden border border-kushnath-border bg-kushnath-secondary/50 shrink-0">
                          <img
                            alt={item.name}
                            className="w-full h-full object-cover"
                            src={item.image || 'https://res.cloudinary.com/dv9iswy2f/image/upload/v1748095974/images_3_y62b89.jpg'}
                          />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-kushnath-foreground line-clamp-1">{item.name}</p>
                          <p className="text-xs text-kushnath-muted-foreground">Qty: {item.quantity}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-semibold text-kushnath-foreground">₹{(item.discountPrice * item.quantity).toFixed(2)}</p>
                        {item.discountPrice < item.product_price && (
                          <p className="text-xs text-kushnath-muted-foreground line-through">₹{(item.product_price * item.quantity).toFixed(2)}</p>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
              <div className="space-y-2 py-4 border-t border-b border-kushnath-border font-sans text-kushnath-foreground/90">
                <div className="flex justify-between">
                  <p>Subtotal</p>
                  <p className="font-medium">₹{subtotal.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p>Shipping</p>
                  <p className="font-medium">{shippingCost === 0 ? 'Free' : `₹${shippingCost.toFixed(2)}`}</p>
                </div>
                {totalSavings > 0 && (
                  <div className="flex justify-between">
                    <p>You Save</p>
                    <p className="font-medium text-kushnath-accent">₹{totalSavings.toFixed(2)}</p>
                  </div>
                )}
              </div>
              <div className="flex justify-between text-lg font-semibold text-kushnath-foreground mt-4 mb-6">
                <p>Total</p>
                <p>₹{finalTotal.toFixed(2)}</p>
              </div>
              <Button
                type="submit"
                size="lg"
                className="w-full bg-kushnath-accent hover:bg-kushnath-accent/90 text-kushnath-accent-foreground h-12 text-base rounded-md font-semibold"
                disabled={isProcessing || razorpayLoading}
              >
                {isProcessing ? (formData.paymentMethod === 'razorpay' ? 'Processing Payment...' : 'Placing Order...') : 'Place Order'}
              </Button>
              {paymentError && (
                <div className="text-red-600 text-sm mt-2 text-center">{paymentError}</div>
              )}
              <Button asChild variant="link" className="w-full mt-3 text-kushnath-primary hover:text-kushnath-accent">
                <Link to="/cart">
                  <ArrowLeft className="mr-2 h-4 w-4" /> Return to Cart
                </Link>
              </Button>
            </div>
          </motion.div>
        </form>
      </div>
    </div>
  );
};

export default AyurvedaCheckoutPage;
