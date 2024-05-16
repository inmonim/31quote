import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import backendApi from "../api/axiosInstance";
import GoToHomeButton from "../components/GoToHomButton";

function UserLogin() {
  const navigate = useNavigate()

  const goToHomButtonClick = () => {
    setTimeout(() => {navigate('/')}, 200)
  }

  const [ loginId, setLoginId ] = useState('')
  const [ password, setPassword ] = useState('')

  const handleLoginId = (e) => {
    setLoginId(e.target.value)
  }

  const handlePassword = (e) => {
    setPassword(e.target.value)
  }

  const submitLoginData = async (e) => {
    console.log(loginId, password)
    e.preventDefault();
    
    await backendApi.post(
      "/user/login",
      {
        username : loginId,
        password : password
      },
      {
        headers: {
          "Content-Type" : "application/x-www-form-urlencoded"
        }
      }
    ).then((response) => {
      console.log(response)
      localStorage.setItem('accessToken', response.data.access_token)
      }
    ).then(() => {
      const access_token = localStorage.getItem('accessToken')
      console.log(access_token)
    })
    .catch((error) => {
      console.log(error)
    })
  }

  return (
    <div>
      <div className="container mx-auto px-20 py-20">
        <form className="grid justify-center" onSubmit={submitLoginData}>
          <p>ID</p>
          <input value={loginId} onChange={(e) => handleLoginId(e)} type="text" className="border-2 rounded-md"></input>
          <p>비밀번호</p>
          <input value={password} onChange={(e) => handlePassword(e)} type="password" className="border-2 rounded-md"></input>
          <button type="submit">로그인</button>
        </form>
        </div>
      <button onClick={goToHomButtonClick}>
        <GoToHomeButton/>
      </button>
    </div>
  )
}

export default UserLogin