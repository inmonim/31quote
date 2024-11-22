import React from "react";
import './Home.css'
import { useState, useEffect } from "react";

import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import { getAllRandomQuote, getCategoryListRnadomQuote, getCategoryList } from "@/apis/QuoteAPI";


export function Home() {

  const navigate = useNavigate();

  // quote data
  const [quoteId, setQuoteId] = useState('');
  const [koSentence, setKoSentence] = useState('');
  const [enSentence, setEnSentence] = useState('');
  const [category, setCategory] = useState('');
  const [speakerKoName, setSpeakerKoName] = useState('');
  const [speakerOrgName, setSpeakerOrgName] = useState('');
  // const [reference, setReference] = useState('');

  // option
  const [textAlign, setTextAlign] = useState('');

  // category
  const getCategory = () => {
    getCategoryList().then((response) => {
      const data = response.data
      localStorage.setItem("user_category", JSON.stringify(data))
      return data
    })
  }

  const [userCategory, setUserCategory] = useState(
    () => JSON.parse(localStorage.getItem("user_category")) || getCategory()
  )

  const containerVariants = {
    hidden: { opacity: 0 }, // 초기 상태 (투명)
    visible: {
      opacity: 1,          // 최종 상태 (보이기)
      transition: {
        staggerChildren: 0.2, // 자식 요소 간 애니메이션 간격
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: -30 }, // 위에서 아래로
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }, // 천천히 나타남
  };


  const handleSwipe = (event, info) => {
    event.preventDefault();
    // 오른쪽으로 스와이프 하면 options 화면으로 이동
    console.log(info.offset.y)
    if (info.offset.x < -100) {
      navigate("/options");
    } else if (info.offset.y > 15) {
      
      window.location.reload()
    }
  };

  const setQuoteData = (data) => {
    setQuoteId(data.quote_id)
    setKoSentence(data.ko_sentence)
    setEnSentence(data.en_sentence)
    setCategory(data.category.category)
    setSpeakerKoName(data.speaker.ko_name)
    setSpeakerOrgName(data.speaker.org_name)
  }

  useEffect(() => {
    setTextAlign(localStorage.getItem("alignment") || "center")
    if (userCategory.length == 14 || !userCategory) {
      getAllRandomQuote().then((response) => {  
        setQuoteData(response.data)
      })
    } else {
      const categorys = userCategory.map((item) => item.category_id);
        getCategoryListRnadomQuote(categorys).then((response) => {
          setQuoteData(response.data)
    })
  }}, [userCategory]);

  return (
      <motion.div
        className="home"
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        onPanEnd={handleSwipe}
        initial={{ x: 0 }}
        animate={{ x: 0 }}
        exit={{ x: "-100%" }}
        style={{
          height: "100vh",
          justifyContent: "center"
        }}
      >
      <motion.div style={{ textAlign: textAlign}}
          className="animated-text-container"
          variants={containerVariants} // 부모 애니메이션
          initial="hidden"            // 초기 상태
          animate="visible"           // 최종 상태
        >
          <div>
          <motion.h2 variants={itemVariants}>{koSentence}</motion.h2>
          <motion.h3 variants={itemVariants}>{enSentence}</motion.h3>
          <motion.h3 variants={itemVariants}>{speakerKoName}</motion.h3>
          <motion.p variants={itemVariants}>{speakerOrgName}</motion.p>
          {/* <p>&lt;{reference}&gt;중에서</p> */}
          <motion.p variants={itemVariants}>{category}에 관하여</motion.p>
          </div>
      </motion.div>
    </motion.div>
  )
}