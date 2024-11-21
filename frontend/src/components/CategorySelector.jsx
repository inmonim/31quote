import { React, useState, useEffect } from "react"

import { motion } from "framer-motion";

import { getCategoryList } from "@/apis/QuoteAPI"

import "./CategorySelector.css"


function CategorySelector({ isOpen, onClose }) {

  const [categories, setCategories] = useState([]);
  const [userCategories, setUserCategories] = useState([]);
  const [exit, setExit ] = useState(false)

  const toggleCategory = (category) => {
    setUserCategories((prev) => {
      // 이미 선택된 경우
      if (prev.some((prevCategory) => prevCategory.category_id === category.category_id)) {
        // 요소가 1개일 경우 제거를 막음
        if (prev.length === 1) {
          alert("1개 이상의 카테고리를 선택해야해요!")
          return prev; // 아무 것도 하지 않음
        }
        // 요소가 2개 이상인 경우 제거
        return prev.filter((prevCategory) => prevCategory.category_id !== category.category_id);
      }
  
      // 선택되지 않은 경우 추가
      return [...prev, category];
    });
  };

  const handleClose = () => {
    setExit(true)
    setTimeout(() => {
      setExit(false),
      onClose()
    }, 500)
  }

  const handleApply = () => {
    localStorage.setItem('user_category', JSON.stringify(userCategories))
    handleClose()
  };

  useEffect(() => {
    if (isOpen) {
      getCategoryList().then((response) => {
        const data = response.data
        setCategories(data)
        setUserCategories(() => {
          try {
            return JSON.parse(localStorage.getItem("user_category"))
          } catch {
            return data
          }
        })
      })
    }
  }, [isOpen])

  return (
    isOpen && (
      <div>
        <div className={`overlay ${exit ? "exit" : ""}`} onClick={() => handleClose()}></div>
        <motion.div
          className="modal-overlay"
          initial={{ y: "100%" }}
          animate={{ y: exit ? "100%" : 0 }}
          exit={{ y: "100%" }}
          transition={{
            duration : 0.65,
            ease : "easeInOut"
          }}
        >
          <h3>보고 싶은 카테고리를 선택해주세요</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", justifyContent: "space-evenly"}}>
            <button className="long-button all-select-button" onClick={
              () => setUserCategories(categories)}>
              전부 볼래요!
            </button>
            {categories.map((category) => (
              <button className={`categoryButton ${
                userCategories.some((userCategory) => userCategory.category_id === category.category_id
              ) ? "selected" : ""}`}
                key={category.category_id}
                onClick={() => toggleCategory(category)}
              >
                {category.category}
              </button>
            ))}
          </div>
          <button
            className="long-button apply-button"
            onClick={handleApply}
          >
            저장
          </button>
          <button
            className="long-button cancle-button"
            onClick={handleClose}
          >
            취소
          </button>
        </motion.div>
      </div>
    )
  );
}

export default CategorySelector