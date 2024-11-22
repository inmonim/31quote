import { React, useEffect, useState } from "react"

import { motion } from "framer-motion"

import "./QuoteExample.css"

function QuoteExample( {textAlign} ) {

  const defaultQuoteViewSetting = () => {

    const defaultQuoteViewSet =
      {"한글 명언" : true,
      "영어 번역" : true,
      "말한 사람" : true,
      "말한 사람 본명" : true,
      "출처" : true,
      "카테고리" : true
      }

    const quoteViewSet = () => {
      let set = {}
      if (localStorage.getItem("quote_view_setting")) {
        try {
          set = JSON.parse(localStorage.getItem("quote_view_setting"))
        } catch {
          set = defaultQuoteViewSet
        }
      } else {
        set = defaultQuoteViewSet
      }
      localStorage.setItem("quote_view_setting", JSON.stringify(set))
      return set
    }
    
    return quoteViewSet()
  }

  const [isSettingOpen, setIsSettingOpen ] = useState(false)

  const [quoteViewSetting, setQuoteViewSetting] = useState(
    defaultQuoteViewSetting()
  )

  const toggleQuoteViewSetting = (key) => {
    setQuoteViewSetting(({...quoteViewSetting, [key] : !quoteViewSetting[key]}))
    localStorage.setItem("quote_view_setting", JSON.stringify(({...quoteViewSetting, [key] : !quoteViewSetting[key]})))
  }

  const quoteContainerVariants = {
    hidden: { opacity: 0 }, // 초기 상태 (투명)
    visible: {
      opacity: 1,          // 최종 상태 (보이기)
      transition: {
        staggerChildren: 0.2, // 자식 요소 간 애니메이션 간격
      },
    },
  };

  const quoteItemVariants = {
    hidden: { opacity: 0, y: -30 }, // 위에서 아래로
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }, // 천천히 나타남
  };

  const settingContainerVariants = {
    hidden : { opacity : 0, y: -50},
    visible : {
      opacity: isSettingOpen ? 1 : 0,
      y : 0,
      transition : { duration : 0.6 }
    }
  }

  useEffect(() => {

  },[quoteViewSetting])

  return (
    <div>
      <motion.div style={{ textAlign: textAlign}}
        key={textAlign}
        className="animated-text-container"
        variants={quoteContainerVariants} // 부모 애니메이션
        initial="hidden"            // 초기 상태
        animate="visible"           // 최종 상태
      >
        <div className="example-quote">
          {quoteViewSetting["한글 명언"] && <motion.p className="quote ko-sen"variants={quoteItemVariants}>사랑은 그 자체로 충분하다.</motion.p>}
          {quoteViewSetting["영어 번역"] && <motion.p className="quote en-sen" variants={quoteItemVariants}>Love is sufficient unto love.</motion.p>}
          {quoteViewSetting["말한 사람"] && <motion.p className="quote ko-speak" variants={quoteItemVariants}>칼릴 지브란</motion.p>}
          {quoteViewSetting["말한 사람 본명"] && <motion.p className="quote org-speak" variants={quoteItemVariants}>Gibran Kahlil Gibran</motion.p>}
          {quoteViewSetting["출처"] && <motion.p className="quote ref" variants={quoteItemVariants}>&lt;예언자&gt;중에서</motion.p>}
          {quoteViewSetting["카테고리"] && <motion.p className="quote category" variants={quoteItemVariants}>사랑에 관하여</motion.p>}
        </div>
      </motion.div>
      <hr></hr>
      <motion.div>
        <motion.button 
          style={{margin:10}}
          onClick={() => setIsSettingOpen((prev) => prev ? false : true)}
        >
          {isSettingOpen ? "지금이 좋아요!" : "표시될 항목을 바꾸고 싶어요!"}
        </motion.button>
        { isSettingOpen &&
        <motion.div
          className="setting-button-container"
          style={{justifyContent:"center"}}
          initial="hidden"
          animate="visible"
          variants={settingContainerVariants}
        >

          {Object.entries(quoteViewSetting).map(([key, val]) => (
            <button
              className={`setting-button ${val ? "selected" : ""}`}
              key={key}
              onClick={() => toggleQuoteViewSetting(key)}
            >
              {key}
            </button>
          ))}
        </motion.div>
        }
      </motion.div>
    </div>
  )
}

export default QuoteExample