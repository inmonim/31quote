import { React } from "react"

import { motion } from "framer-motion"

function QuoteExample( {textAlign} ) {

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

  return (
    <div>
      <motion.div style={{ textAlign: textAlign}}
        className="animated-text-container"
        variants={containerVariants} // 부모 애니메이션
        initial="hidden"            // 초기 상태
        animate="visible"           // 최종 상태
      >
        <div className="example-quote">
          <motion.p className="ko-sen" variants={itemVariants}>사랑은 그 자체로 충분하다.</motion.p>
          <motion.p className="en-sen" variants={itemVariants}>Love is sufficient unto love.</motion.p>
          <motion.p className="ko-speak"variants={itemVariants}>칼릴 지브란</motion.p>
          <motion.p className="org-speak" variants={itemVariants}>Gibran Kahlil Gibran</motion.p>
          <motion.p className="ref" variants={itemVariants}>&lt;예언자&gt;중에서</motion.p>
          <motion.p className="category" variants={itemVariants}>사랑에 관하여</motion.p>
        </div>
      </motion.div>
    </div>
  )
}

export default QuoteExample