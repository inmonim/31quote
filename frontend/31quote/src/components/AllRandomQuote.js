import backendApi from '../api/axiosInstance'
import React, { useState, useEffect } from 'react'

function AllRandomQuoteComp() {
  
  const [quoteID, setQuoteID] = useState('')
  const [koSentence, setKoSentence] = useState('')
  const [orgSentence, setOrgSentence] = useState('')
  const [speakerName, setSpeakerName] = useState('')
  const [speakerOrgName, setSpeakerOrgName] = useState('')
  const [source, setSource] = useState('')
  const [subtext, setSubtext] = useState('')
  const [category, setCategory] = useState('')

  useEffect(() => {
    
    backendApi.get('http://localhost:5051/api/v1/quote/getAllRandomQuote')
      .then(response => {
        const quoteData = response.data;
        setQuoteID(quoteData.quote_id)
        setKoSentence(quoteData.quote_sentence.ko_sentence)
        setOrgSentence(quoteData.quote_sentence.org_sentence)
        setSpeakerName(quoteData.quote_speaker.speaker_name)
        setSpeakerOrgName(quoteData.quote_speaker.speaker_org_name)
        setSource(quoteData.quote_source)
        setSubtext(quoteData.quote_subtext)
        setCategory(quoteData.quote_category.category)
      })
      .catch(error => {
        console.log(error)
      })
  }, [])

  return (
    <div>
      <div class="container mx-auto rounded-lg shadow border-2 border-green-300">
        <p>{koSentence}</p>
        <p>{orgSentence}</p>
        <p>{speakerName}</p>
        <p>{speakerOrgName}</p>
        <p>{source}</p>
      </div>
    </div>
  )
}

export default AllRandomQuoteComp