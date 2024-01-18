import React from "react";
import { useState, useEffect } from "react";
import { storage } from "../firebase";
import {
  ref,
  getDownloadURL,
  listAll,
} from "firebase/storage";

export default function Signup(){
  const [imageUrls, setImageUrls] = useState([]);
  const imagesListRef = ref(storage, "images/");

  useEffect(() => {
    listAll(imagesListRef).then((response) => {
      response.items.forEach((item) => {
        getDownloadURL(item).then((url) => {
          setImageUrls((prev) => [...prev, url]);
        });
      });
    });
  });

  return (
    <div className="App">
      {imageUrls.map((url) => {
        return <img src={url} alt ="Reference"/>;
      })}
    </div>
  );
}