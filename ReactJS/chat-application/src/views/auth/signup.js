import React, { useContext, useState } from 'react';
// import axios from 'axios';
// import {useAuth} from './jwtcontext';
import jwtcontext from '../../context/jwtcontext';
import{ useNavigate} from 'react-router-dom';
import companyLogo from '../../assets/images/auth/signup.png';
import { Link } from 'react-router-dom';
import '../../assets/css/logpage/signup.css';

const SignUp = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPasswordMatchError, setShowPasswordMatchError] = useState(false);
    const [passwordsMatch, setPasswordsMatch] = useState(false);
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
    const [error, setError] = useState(null);

    const { signup } = useContext(jwtcontext);

    const navigate = useNavigate();

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
        setPasswordsMatch(event.target.value === confirmPassword);
        setShowPasswordMatchError(event.target.value !== confirmPassword);
    };

    const handleConfirmPasswordChange = (event) => {
        setConfirmPassword(event.target.value);
        setPasswordsMatch(event.target.value === password);
        setShowPasswordMatchError(event.target.value !== password);
    };

    const handleTogglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    const handleToggleConfirmPasswordVisibility = () => {
        setConfirmPasswordVisible(!confirmPasswordVisible);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!passwordsMatch) {
            setShowPasswordMatchError(true);
            return;
        }
        try {
            await signup(firstName, lastName, phoneNumber,email,password);
            setError(null);
            navigate('/signin')
        } catch (error) {
            setError('Failed to sign up. Please try again.');
            console.error(error);
        }
    };

    return (
        <div className='container-signup'>
            <section className='img-logo-section-left'>
                <img className='img-company-logo' src={companyLogo} alt="Company Logo" />
            </section>
            <div className='signup-right'>
                <div className='square'>
                    <h1 className='heading-signup'>Create an Account</h1>
                    <p className='text'>Please provide your details to sign up.</p>
                    <form onSubmit={handleSubmit}>
                        <div className='input-first-name-signup'>
                            <input
                                type="text"
                                className='form-control-signup'
                                placeholder='First Name*'
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                required
                            />
                        </div>
                        <div className='input-last-name-signup'>
                            <input
                                type="text"
                                className='form-control-signup'
                                placeholder='Last Name*'
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                required
                            />
                        </div>
                        <div className='input-phone-number-signup'>
                            <input
                                type="text"
                                className='form-control-signup'
                                placeholder='Phone Number*'
                                value={phoneNumber}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                                required
                            />
                        </div>
                        <div className="input-email-signup">
                            <input
                                type="email"
                                className="form-control-signup"
                                placeholder="Email address*"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="password-input-container-signup">
                            <input
                                type={passwordVisible ? 'text' : 'password'}
                                className="password-input-signup"
                                placeholder="Password*"
                                value={password}
                                onChange={handlePasswordChange}
                                required
                            />
                            <button
                                type="button"
                                className="toggle-visibility-signup"
                                onClick={handleTogglePasswordVisibility}>
                                {passwordVisible ? '🔒' : '👁️'}
                            </button>
                        </div>
                        <div className="password-input-container-signup">
                            <input
                                type={confirmPasswordVisible ? 'text' : 'password'}
                                className="confirm-password-form-control-signup"
                                placeholder="Confirm Password*"
                                value={confirmPassword}
                                onChange={handleConfirmPasswordChange}
                                required
                            />
                            <button
                                type="button"
                                className="toggle-visibility-signup"
                                onClick={handleToggleConfirmPasswordVisibility}>
                                {confirmPasswordVisible ? '🔒' : '👁️'}
                            </button>
                            {showPasswordMatchError && <p style={{ color: 'red' }}>
                                Passwords do not match!</p>}
                        </div>
                        {passwordsMatch && (
                            <div className="popup-signup">
                                <p>Passwords match!</p>
                            </div>
                        )}
                        {error && <p style={{ color: 'red' }}>{error}</p>}
                        <div className='container-for-login-signup'>
                            <section className='sign-in-section-signup'>
                                <div>
                                    <button type="submit" onClick={handleSubmit} className='button-for-signup-signup'>Sign up</button>
                                </div>
                            </section>
                            <section className='forgot-password-button-section'>
                                <div className='signin-button-signup'>
                                    <p className='p-for-signin'>Already have an account?
                                        <Link to="/signin" className="f-w-400"> Sign In</Link>
                                    </p>
                                </div>
                            </section>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SignUp;
