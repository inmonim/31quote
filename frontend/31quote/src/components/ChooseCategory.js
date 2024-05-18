import React, { useState, useEffect } from "react";
import ReactModal from "react-modal";

import backendApi from "../api/axiosInstance";

ReactModal.setAppElement('#root');

const ChooseCategory = ({isOpen, ModalClose}) => {

  const [ categoryItem, setCategoryItem ] = useState([])
  const [ uncheckedCategoryItem, setUncheckedCategoryItem ] = useState([])
  const [ usersCategoryItem, setUsersCategoryItem ] = useState([])

  useEffect(() => {
    if (isOpen) {
      // 유저의 카테고리 가져오기 및 분류
      backendApi.get('/user_setting/getAllCategory')
      .then((response) => {
        setCategoryItem(response.data)
        const allCategory = response.data

        backendApi.get('/user_setting/getUserCategory')
        .then((userResponse) => {
          setUsersCategoryItem(userResponse.data)
          const usersCategory = userResponse.data
          const uncheckItem = allCategory.filter(cat =>
            !usersCategory.some(userCat => userCat.category_id === cat.category_id)
          )
          setUncheckedCategoryItem(uncheckItem)
          console.log(uncheckItem)
        })
      })
    }
  }, [isOpen])

  return (
    <ReactModal isOpen={isOpen}>
      <div>
        보고 싶은 카테고리를 선택하세용
      </div>
      {uncheckedCategoryItem.map(ucCat => (
        <button className="gap-4" key={ucCat.category_id}>{ucCat.category}</button>
      ))}


      <button onClick={ModalClose}>
        꺼져랏!
      </button>
    </ReactModal>
  );
};

export default ChooseCategory;