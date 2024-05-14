import React from 'react';
import GoToUserButton from '../components/GoToUserButton';

import AllRandomQuoteComp from '../components/AllRandomQuote';


function HomePage() {

  return (
    <div class="relative container px-3 py-4">
      <AllRandomQuoteComp />
      <GoToUserButton/>
    </div>
  )
}

export default HomePage