import { React, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { AlignOptions } from "@/components/AlignOption"
import CategorySelector from "../components/CategorySelector";

import "./Options.css"

function Options() {
  const navigate = useNavigate();

  const [categorySelectorOpen, setCategorySelectorOpen] = useState(false);

  const handleSwipe = (event, info) => {
    // 왼쪽으로 스와이프 하면 홈 화면으로 이동
    if (info.offset.x > 100) {
      navigate("/");
    }
  };

  return (
    <motion.div
      className="options"
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onPanEnd={handleSwipe} // 스와이프 감지
      initial={{ x: "30%" }}
      animate={{ x: 0 }}
      exit={{ x: "100%" }}
      transition={{
        type: "tween",
        duration: 0.3,
        ease: "easeOut", // 또는"easeInOut"
      }}
      style={{
        height: "100vh"
      }}
    >
      <div className="options-container">
        <h2>글을 어느 쪽에 붙일까요?</h2>
        <AlignOptions>
        </AlignOptions>
      </div>
      <div className="options-container">
        <h2>명언 종류를 바꿀래요</h2>
        <button style={{ fontWeight: "bold" }}  onClick={() => setCategorySelectorOpen(true)}>
          받아볼 명언 종류 바꾸기
        </button>
        <CategorySelector isOpen={categorySelectorOpen}
          onClose={() => setCategorySelectorOpen(false)}>
        </CategorySelector>
      </div>

      <h1>Options</h1>
      <p>Swipe left to go back</p>
    </motion.div>
  );
}

export default Options;