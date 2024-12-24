function validateForm() {
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const Flash = document.getElementById('flash');
    
    // Name validation
    // const namePattern = /^[A-Za-z\s-]{2,50}$/;
    // if (!namePattern.test(firstName) || !namePattern.test(lastName)) {
    //   Flash.innerHTML='Please enter a valid first and last name.';
    //   return false;
    // }
    
    // Email validation
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
    Flash.innerHTML='Please enter a valid email address.';
      return false;
    }
    
    // Password validation
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordPattern.test(password)) {
        Flash.innerHTML='Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.';
      return false;
    }
    
    // // Confirm Password validation
    // if (password !== confirmPassword) {
    //   Flash.innerHTML='Passwords do not match.';
    //   return false;
    // }
  
    // If all validations pass
    
    validateOtp();


    return true;
  }
  
