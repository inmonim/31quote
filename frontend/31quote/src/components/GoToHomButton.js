import React from 'react';
import HomeImage from '../assets/home_logo.png'

const GoToHomeButton = () => {
  return (
    <div class="fixed bottom-12 right-12 size-20 ">
      <div class="px-2 py-2 bg-emerald-100 font-bold rounded-full shadow-lg z-50
      transition-transform transform hover:scale-75 hover:bg-emerald-200 duration-300 ease-in-out">
        <img src={HomeImage} alt="home_logo" class="opacity-25"></img>
      </div>
    </div>
  )
}

export default GoToHomeButton;