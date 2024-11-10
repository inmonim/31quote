import React from "react";
import { useState, useEffect } from "react";

import { getAllRandomQuote } from "@/apis/quote_api";


export function Home() {

  const [quoteId, setQuoteId] = useState('');
  const [koSentence, setKoSentence] = useState('');
  const [enSentence, setEnSentence] = useState('');
  const [category, setCategory] = useState('');
  const [speakerKoName, setSpeakerKoName] = useState('');
  const [speakerOrgName, setSpeakerOrgName] = useState('');
  const [reference, setReference] = useState('');

  useEffect(() => {
    getAllRandomQuote().then(response => {
      const data = response.data
      console.log(data)
      setQuoteId(data.quote_id)
      setKoSentence(data.ko_sentence)
      setEnSentence(data.en_sentence)
      setCategory(data.category.category)
      setSpeakerKoName(data.speaker.ko_name)
      setSpeakerOrgName(data.speaker.org_name)
    })
  }, [])
  
  return (
    <div>
      <h3>{koSentence}</h3>
      <p>{enSentence}</p>
      <p>{category}</p>
      <p>{speakerKoName}</p>
      <p>{speakerOrgName}</p>
    </div>
  )
}