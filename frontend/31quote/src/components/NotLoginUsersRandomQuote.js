import backendApi from '../api/axiosInstance'
import React, { useState, useEffect } from 'react'

function NotLoginUsersRandomQuote() {
  
  const [quoteID, setQuoteID] = useState('')
  const [koSentence, setKoSentence] = useState('')
  const [orgSentence, setOrgSentence] = useState('')
  const [speakerName, setSpeakerName] = useState('')
  const [speakerOrgName, setSpeakerOrgName] = useState('')
  const [source, setSource] = useState('')
  const [subtext, setSubtext] = useState('')
  const [category, setCategory] = useState('')

  useEffect(() => {

    // 로그인이 된 상태면 호출 X
    if (localStorage.getItem('accessToken')) {
      return
    }
    
    backendApi.get('/quote/all_random')
      .then(response => {
        const quoteData = response.data;
        console.log(response.data)
        setQuoteID(quoteData.quote_id)
        setKoSentence(quoteData.ko_sentence)
        setOrgSentence(quoteData.org_sentence)
        setSpeakerName(quoteData.speaker.ko_name)
        setSpeakerOrgName(quoteData.speaker.org_name)
        setCategory(quoteData.category.category)
      })
      .catch(error => {
        console.log(error)
      })
  }, [])

  return (
    <div class="container mx-auto p-5 pt-8 rounded-lg shadow border-2 border-green-300">
      <div class="text-2xl mb-5 font-bold">{koSentence}</div>
      <div class="text-lg italic text-gray-500 mb-5">{orgSentence}</div>
      <div class="grid grid-cols-2 gap-4">
        <div></div>
        <div class="text-lg italic font-bold">- {speakerName}</div>
        <div class="text-lg font-semibold">{category}</div>
        <div class="text-lg italic text-gray-500 font-bold">{speakerOrgName}</div>
        <div></div>
        <div>{source}</div>
      </div>
    </div>
  )
}

export default NotLoginUsersRandomQuote