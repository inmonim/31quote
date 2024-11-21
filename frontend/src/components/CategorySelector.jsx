import { React, useState, useEffect } from "react"

import { motion } from "framer-motion";

import { getCategoryList } from "@/apis/QuoteAPI"


function CategorySelector({ isOpen, onClose }) {

  const [categories, setCategories] = useState([]);
  const [userCategories, setUserCategories] = useState([]);

  const toggleCategory = (category) => {
    setUserCategories((prev) =>
      prev.some((prevCategory) => prevCategory.category_id === category.category_id)
        ? prev.filter((prevCategory) => prevCategory.category_id !== category.category_id) // 이미 선택된 경우 제거
        : [...prev, category] // 선택되지 않은 경우 추가
    );
  };

  const handleApply = () => {
    localStorage.setItem('user_category', JSON.stringify(userCategories))
    onClose();
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
      <motion.div
        className="modal-overlay"
        initial={{ y: "100%" }}
        animate={{ y: 0 }}
        exit={{ y: "100%" }}
        style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          width: "92%",
          backgroundColor: "#ffffff",
          boxShadow: "0px -2px 10px rgba(0,0,0,0.2)",
          borderTopLeftRadius: "16px",
          borderTopRightRadius: "16px",
          padding: "16px",
        }}
      >
        <h2>Choose Categories</h2>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
          {categories.map((category) => (
            <button
              key={category.category_id}
              onClick={() => toggleCategory(category)}
              style={{
                width: "80px",
                height: "80px",
                borderRadius: "12px",
                border: "none",
                backgroundColor: userCategories.some((userCategory) => userCategory.category_id === category.category_id )
                  ? "#4CAF50"
                  : "#f0f0f0",
                color: userCategories.some((userCategory) => userCategory.category_id === category.category_id ) ? "#fff" : "#000",
                fontWeight: "bold",
                cursor: "pointer",
              }}
            >
              {category.category}
            </button>
          ))}
        </div>
        <button
          onClick={handleApply}
          style={{
            marginTop: "16px",
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#007BFF",
            color: "#fff",
            fontWeight: "bold",
            cursor: "pointer",
            width: "100%",
          }}
        >
          Apply
        </button>
        <button
          onClick={onClose}
          style={{
            marginTop: "8px",
            padding: "10px 16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: "#fff",
            color: "#000",
            fontWeight: "bold",
            cursor: "pointer",
            width: "100%",
          }}
        >
          Cancel
        </button>
      </motion.div>
    )
  );
}

export default CategorySelector