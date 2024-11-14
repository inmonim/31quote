import React from "react";
import { useState, useEffect } from "react";

import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import { getAllRandomQuote } from "@/apis/quote_api";


export function Home() {

  const [quoteId, setQuoteId] = useState('');
  const [koSentence, setKoSentence] = useState('');
  const [enSentence, setEnSentence] = useState('');
  const [category, setCategory] = useState('');
  const [speakerKoName, setSpeakerKoName] = useState('');
  const [speakerOrgName, setSpeakerOrgName] = useState('');
  // const [reference, setReference] = useState('');

  // option
  const [textAlign, setTextAlign] = useState('');

  const navigate = useNavigate();

  const handleSwipe = (event, info) => {
    event.preventDefault();
    // 오른쪽으로 스와이프 하면 options 화면으로 이동
    if (info.offset.x < -100) {
      navigate("/options");
    }
  };

  useEffect(() => {
    getAllRandomQuote().then(response => {
      setTextAlign(localStorage.getItem("alignment"))
      const data = response.data
      setQuoteId(data.quote_id)
      setKoSentence(data.ko_sentence)
      setEnSentence(data.en_sentence)
      setCategory(data.category.category)
      setSpeakerKoName(data.speaker.ko_name)
      setSpeakerOrgName(data.speaker.org_name)
      // setReference(data.reference.reference_name)
    })
  }, [])

  return (
      <motion.div
        className="home"
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        onPanEnd={handleSwipe}
        initial={{ x: "-30%" }}
        animate={{ x: 0 }}
        exit={{ x: "-100%" }}
        transition={{
          type: "tween",
          duration: 0.3,
          ease: "easeOut", // 또는 "easeInOut"
        }}
        style={{
          height: "100vh",
          justifyContent: "center"
        }}
      >
      <div style={{ textAlign: textAlign}}>
        <div>
          <h2>{koSentence}</h2>
          <h3>{enSentence}</h3>
        </div>
        <div>
          <h3>{speakerKoName}</h3>
          <p>{speakerOrgName}</p>
          {/* <p>&lt;{reference}&gt;중에서</p> */}
          <p>{category}에 관하여</p>
        </div>
      </div>
    </motion.div>
  )
}