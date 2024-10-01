import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'

import GoToUserButton from '../components/GoToUserButton';
import NotLoginUsersRandomQuote from '../components/NotLoginUsersRandomQuote';
import UsersCheckCategoryQuote from '../components/UsersCheckCategoryQuote';
import ChooseCategory from '../components/ChooseCategory';


function HomePage() {
  const navigate = useNavigate();

  const GoToUserButtonClick = () => {
    setTimeout(() => {navigate('/login');}, 200);
  };
  
  const [ isCategoryModalOpen, setIsCategoryModalOpen ] = useState(false);
  const [ isLogined, setIsLogined ] = useState(false);

  const openModal = () => {
    isCategoryModalOpen ? setIsCategoryModalOpen(false) : setIsCategoryModalOpen(true)
  }

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      setIsLogined(true);
    }
  }, []);

  return (
    <div class="relative container px-3 py-4">
      {isLogined ? (
        <UsersCheckCategoryQuote/>
      ) : (
        <NotLoginUsersRandomQuote />
      )}

      <button onClick={openModal}>openmodal</button>
      <ChooseCategory isOpen={isCategoryModalOpen} ModalClose={openModal}/>

      <button onClick={GoToUserButtonClick}>
        <GoToUserButton />
      </button>
    </div>
  )
}

export default HomePage