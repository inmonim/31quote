import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

function Options() {
  const navigate = useNavigate();

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
      initial={{ x: "100%" }}
      animate={{ x: 0 }}
      exit={{ x: "100%" }}
      style={{
        height: "100vh"
      }}
    >
      <h1>Options</h1>
      <p>Swipe left to go back</p>
    </motion.div>
  );
}

export default Options;