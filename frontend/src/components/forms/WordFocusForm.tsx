import { TiTick, TiTickOutline } from "react-icons/ti";
import { CardType, ReadCardDTO, ReviewType, WordDTO } from '../../types/dto';
import { CardTypeIconMap } from "../../constants/IconMapper";
import { useState } from "react";
import { MdKeyboardArrowDown, MdKeyboardArrowUp } from "react-icons/md";


const WordFocusForm = (props: { word:WordDTO, readCardDto: ReadCardDTO, getReadCardDto: ()=>void, addCardType: (cardType:CardType, reviewType:ReviewType)=>void, addCardTypeAll: ()=>void, removeCardType:(cardType:CardType, reviewType:ReviewType)=>void}) => {
  const word = props.word;
  const [openOption, setOpenOption] = useState<number>(-1);
  console.log(props.readCardDto)

  const onCheckboxChange = (cardType: CardType, reviewType:ReviewType, checked: boolean) => {
    if (checked) {
      props.addCardType(cardType, reviewType)
    }else{
      props.removeCardType(cardType, reviewType)
    }
  }

  return (
    <>
      <div className="relative bg-base-100 w-7/12 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md m-4">
        <h1 className="text-9xl">{word?.hanzi}</h1>
        <h1 className="text-5xl">{word?.pinyin}</h1>
        <h1 className="text-2xl">{word?.meaning}</h1>
        {props.readCardDto.card.length !== 0? (
          <span className="text-base-content text-md absolute right-2 top-2">
            <TiTick className="text-3xl"/>
          </span>
        ) : (
          <span className="text-base-content text-md absolute right-2 top-2">
            <TiTickOutline className="text-3xl"/>
          </span>
        )}
      </div>

      <div className="relative w-full flex-1  flex flex-col m-4">
        {
          props.readCardDto.card.length === 0 && <><div className="absolute bg-slate-700 top-0 left-0 h-full w-full"/>
          <div className="absolute  top-0 left-0 h-full w-full flex justify-center content-center items-center">
          <button className="bg-base-100 rounded-md py-1 px-4 m-2 text-base-content text-center select-none" onClick={()=>{props.addCardTypeAll()}}>Learn</button>
          </div></>
        }
        
        <div className="rounded-md w-full h-56 flex flex-col  text-left">
          <label>Cards:</label>
          <div className="flex flex-col bg-slate-200 p-1 my-2 h-40 rounded-md overflow-y-scroll">
            {
              [...new Set(props.readCardDto.card.map(card=>card.card_type))].map((cardType, index) => (
                <div className="flex flex-col mb-1">
                <label key={cardType} className="label bg-base-100 border rounded-md h-8 cursor-pointer" onClick={()=>{setOpenOption(openOption=>openOption===index?-1:index)}}>
                    <span className="label-text flex flex-row text-xl items-center">
                      {CardTypeIconMap({cardType: cardType})}
                      {CardType[cardType]}
                      {props.readCardDto.card.filter(card => card.card_type === cardType).map((card) =>(
                        <>
                        {card.is_disabled === false?<TiTick className="text-2xl"/>:<TiTickOutline className="text-2xl"/>}
                        </>
                      ))
                    }
                    </span>

                {openOption!==index?<MdKeyboardArrowDown/>:<MdKeyboardArrowUp/>}
                </label>
                <div className={`overflow-y-hidden ${openOption == index?"h-fit":"h-0"}`}>
                    {
                [...new Set(props.readCardDto.card.filter(card=>card.card_type === cardType).map(card=>card.review_type))].map((reviewType) => (
                  <div className="flex flex-row bg-slate-100 items-center rounded select-none" >
                    <input key={cardType+reviewType} type="checkbox" className="checkbox mx-2 my-1" onChange={e=>{onCheckboxChange(cardType, reviewType, e.target.checked)}}
                    checked={props.readCardDto.card.some(card=>card.card_type === cardType && card.review_type === reviewType && card.is_disabled === false) }
                    />
                    {ReviewType[reviewType]}
                    </div>
                ))
              }
              </div>
                </div>
              ))
            }
            
          </div>
        </div>
        <div className="bg-blue-100 w-full h-full"></div>
      </div>
    </>
  );
};

export default WordFocusForm;
