import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'

import GoToUserButton from '../components/GoToUserButton';
import NotLoginUsersRandomQuote from '../components/NotLoginUsersRandomQuote';
import UsersCheckCategoryQuote from '../components/UsersCheckCategoryQuote';


function HomePage() {
  const navigate = useNavigate();

  const GoToUserButtonClick = () => {
    setTimeout(() => {navigate('/login');}, 200)
  };

  const [ isLogined, setIsLogined ] = useState(false)

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');

    if (accessToken) {
      setIsLogined(true);
    }

    console.log(accessToken)
  }, []);



  return (
    <div class="relative container px-3 py-4">
      {isLogined ? (
        <UsersCheckCategoryQuote/>
      ) : (
        <NotLoginUsersRandomQuote />
      )}
      <button onClick={GoToUserButtonClick}>
        <GoToUserButton />
      </button>
    </div>
  )
}

export default HomePage