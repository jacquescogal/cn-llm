import {  useEffect, useState } from "react";
import { ReadCardDTO, WordDTO } from '../../types/dto';
import { IoIosAddCircle, IoIosRemoveCircle } from "react-icons/io";
import { TiTick, TiTickOutline } from "react-icons/ti";
import Modal from "../modal/Modal";
import WordFocusForm from "../forms/WordFocusForm";
import { createCard, createCardAll, deleteCardOfWordCardTypeReviewType, getCardById } from "../../services/card-api";


const ExploreCard = (props: { word: WordDTO; searchQuery: string}) => {
  const [isLearnt, setIsLearnt] = useState<boolean>(props.word.is_learnt);
  const [readCardDto, setReadCardDto] = useState<ReadCardDTO>({
    word: props.word,
    card: [],
  });
  const word = props.word;

  

  useEffect(() => {
    setIsLearnt(word.is_learnt);
  }, [word]);

  const getReadCardDto = async () => {
    try {
      const response: ReadCardDTO = await getCardById(word.word_id);
      setReadCardDto(response);
    } catch (error) {
      console.error(error)
    }
  }

  const addCardTypeAll = async () => {
    try {
      const response: ReadCardDTO = await createCardAll(word.word_id);
      setReadCardDto(response);
      setIsLearnt(true);
    } catch (error) {
      console.error(error)
    }
  }

  const addCardType = async (cardType: number, reviewType:number) => {
    try {
      const response: ReadCardDTO = await createCard(word.word_id, cardType, reviewType);
      const currentCardList = readCardDto.card;
      for (const cardDto of response.card){
        // replace the card if it already exists else add it
        const index = currentCardList.findIndex((card)=>card.card_type === cardDto.card_type && card.review_type === cardDto.review_type);
        if (index !== -1){
          currentCardList[index] = cardDto;
        }
        else{
          currentCardList.push(cardDto);
        }
      }
      setReadCardDto({...readCardDto, card: currentCardList});
    } catch (error) {
      console.error(error)
    }
  }

  const removeCardType = async (cardType: number, reviewType:number) => {
    console.log(cardType, reviewType)
    try {
      await deleteCardOfWordCardTypeReviewType(word.word_id, cardType, reviewType);
      const currentCardList = readCardDto.card;
      const index = currentCardList.findIndex((card)=>card.card_type === cardType && card.review_type === reviewType);
      if (index !== -1){
        currentCardList[index].is_disabled = true;
      }
      setReadCardDto({...readCardDto, card: currentCardList});
    } catch (error) {
      console.error(error)
    }
  }
  return (
    <div
      className={
        "relative bg-base-100 border-black border-4 h-48 w-80 rounded-xl shadow-inset shadow-md group " +
        `${isLearnt ? "bg-green-100" : "bg-yellow-50"}`
      }>
        <Modal modalId={`explore-${word.hanzi}`} reactNode={
      <div className="group-hover:bg-black group-hover:opacity-70 opacity-0 rounded-md absolute w-full h-full cursor-pointer">
        {isLearnt?<IoIosRemoveCircle className=" text-white text-7xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 " />:<IoIosAddCircle className=" text-white text-7xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 " />}
      </div>
      } 
      form={
        <WordFocusForm word={word} readCardDto={readCardDto} getReadCardDto={getReadCardDto} addCardType={addCardType} addCardTypeAll={addCardTypeAll} removeCardType={removeCardType}/>
      }
      onClickModal={()=>{getReadCardDto()}}
      />
      <div className="w-full h-full select-none">
        <div className="absolute left-2 top-2">
          <h1 className="text-base-content text-xs select-none">
            {word.hsk_level}:{word.word_id}
          </h1>
        </div>
        {isLearnt === true ? (
          <span className="text-base-content text-md absolute right-2 top-2">
            <TiTick className="text-2xl"/>
          </span>
        ) : (
          <span className="text-base-content text-md absolute right-2 top-2">
            <TiTickOutline className="text-2xl"/>
          </span>
        )}

        <div className="w-full h-full flex justify-center  items-center mt-2">
          <div className="flex flex-col">
            <h1 className="text-base-content text-7xl">{word.hanzi}</h1>
            <span className="text-base-content text-md">
              {highLight(word.pinyin, props.searchQuery)}
            </span>
            <span className="text-base-content text-md">{word.meaning}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const highLight = (word: string, searchQuery: string): React.ReactNode => {
  const index = removePinyinTones(word).indexOf(searchQuery);
  if (index === -1 || searchQuery === "") {
    return word;
  }
  return (
    <>
      {word.slice(0, index)}
      <span className="bg-primary">
        {word.slice(index, index + searchQuery.length)}
      </span>
      {
        (index + searchQuery.length < word.length) && 
          highLight(word.slice(index + searchQuery.length), searchQuery)
      }
    </>
  );
};
function removePinyinTones(pinyin: string): string {
  const toneMap: { [key: string]: string } = {
    ā: "a",
    á: "a",
    ǎ: "a",
    à: "a",
    ē: "e",
    é: "e",
    ě: "e",
    è: "e",
    ī: "i",
    í: "i",
    ǐ: "i",
    ì: "i",
    ō: "o",
    ó: "o",
    ǒ: "o",
    ò: "o",
    ū: "u",
    ú: "u",
    ǔ: "u",
    ù: "u",
    ǖ: "u",
    ǘ: "u",
    ǚ: "u",
    ǜ: "u",
    ü: "u",
    ń: "n",
    ň: "n",
    "": "m",
  };

  return pinyin.replace(
    /[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüńň]/g,
    (match) => toneMap[match] || match
  );
}

export default ExploreCard;
