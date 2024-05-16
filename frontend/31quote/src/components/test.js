import { React, useState, useEffect } from "react";
import backendApi from "../api/axiosInstance";

function Test() {

  const [ koSentence, setKoSentence ] = useState('')

  useEffect(() => {
    backendApi.get('/quote/getQuoteByUsersAllCategory')
    .then((response) => {
      setKoSentence(response.data.quote_sentence.ko_sentence)
    }).catch((error) => {
      console.log(error)
    })
  }, [])

  return (
    <div>
      {koSentence}
    </div>
  )
}

export default Test;