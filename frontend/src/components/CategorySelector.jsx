import { React, useState, useEffect } from "react"

import { getCategoryList } from "@/apis/QuoteAPI"

export function CategorySelector() {

  const getCategory = () => {
    getCategoryList().then((response) => {
      const data = response.data
      localStorage.setItem("user_category", data)
    })
  }

  const [category, setCategory] = useState(
    () => localStorage.getItem("user_category") || getCategory()
  )

  return (
    <div>
      {category}
    </div>
  )
}