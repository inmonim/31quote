import React, { useEffect, useState } from "react";

import "./AlignOption.css"

export function AlignOptions() {
  // 초기값을 localStorage에서 가져오거나 기본값 'center' 설정
  const [alignment, setAlignment] = useState(
    () => localStorage.getItem("alignment") || "center"
  );

  // 로컬 스토리지에 저장
  const saveToLocalStorage = (newAlignment) => {
    setAlignment(newAlignment);
    localStorage.setItem("alignment", newAlignment);
  };

  return (
    <div>
      <h2>글을 어느 쪽에 붙일까요?</h2>
      <div className="button-group" style={{ display: "flex", justifyContent: "center", marginTop: "5px" }}>
        {/* 왼쪽 정렬 버튼 */}
        <button
          className={`button ${alignment === "left" ? "active" : ""}`}
          onClick={() => saveToLocalStorage("left")}
        >
          좌측
        </button>

        {/* 가운데 정렬 버튼 */}
        <button
          className={`button ${alignment === "center" ? "active" : ""}`}
          onClick={() => saveToLocalStorage("center")}
        >
          중앙
        </button>

        {/* 오른쪽 정렬 버튼 */}
        <button
          className={`button ${alignment === "right" ? "active" : ""}`}
          onClick={() => saveToLocalStorage("right")}
        >
          우측
        </button>
      </div>
    </div>
  );
};
