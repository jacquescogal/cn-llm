import { TiTick, TiTickOutline } from "react-icons/ti";
import { CardType, ReadCardDTO, WordDTO } from '../../types/dto';
import { RiPinyinInput } from "react-icons/ri";
import { FaCheckDouble } from "react-icons/fa";
import {  MdOutlineQuestionMark } from "react-icons/md";

interface CardOption {
  name: string;
  type: CardType;
  icon?: React.ReactNode;
}

const CardOptions: CardOption[] = [
  {
    name: "Meaning",
    type: CardType.Meaning,
    icon: <MdOutlineQuestionMark/>,

  },
  {
    name: "Pinyin",
    type: CardType.Pinyin,
    icon: <RiPinyinInput />,
  },
  {
    name: "Hanzi",
    type: CardType.Hanzi,
    icon: "中",
  },
  {
    name: "MCQ",
    type: CardType.MCQ,
    icon: <FaCheckDouble/>,
  },
  // {
  //   name: "Draw",
  //   checked: false,
  //   icon: <MdDraw/>,
  // },
];

const WordFocusForm = (props: { word:WordDTO, readCardDto: (ReadCardDTO), getReadCardDto: ()=>void, addCardType: (cardType:CardType)=>void, addCardTypeAll: ()=>void, removeCardType:(cardType:CardType)=>void}) => {
  const word = props.word;


  const onCheckboxChange = (cardType: CardType, checked: boolean) => {
    if (checked) {
      props.addCardType(cardType)
    }else{
      props.removeCardType(cardType)
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
          props.readCardDto.card.length === 0 && <><div className="absolute bg-black opacity-70 top-0 left-0 h-full w-full"/>
          <div className="absolute  top-0 left-0 h-full w-full flex justify-center content-center items-center">
          <button className="bg-base-100 rounded-md py-1 px-4 m-2 text-base-content text-center select-none" onClick={()=>{props.addCardTypeAll()}}>Learn</button>
          </div></>
        }
        
        <div className="rounded-md w-full h-fit flex flex-col  text-left">
          <label>Cards:</label>
          <div className="flex flex-col bg-base-200 p-1 my-2 h-fit rounded-md">
            {CardOptions.map((option) => (
              <label key={option.name} className="label cursor-pointer bg-base-100 border rounded-md h-8 mb-1">
                <span className="label-text flex flex-row text-lg">
                  {option.icon}
                </span>
                <span className="label-text flex flex-row text-lg w-full">
                  {option.name}
                </span>
                <input type="checkbox" className="checkbox" onChange={e=>{onCheckboxChange(option.type, e.target.checked)}}
                checked={props.readCardDto.card.some(card=>card.card_type === option.type && card.is_disabled === false) }
                />
              </label>
            ))}
          </div>
        </div>
        <div className="bg-blue-100 w-full h-full"></div>
      </div>
    </>
  );
};

export default WordFocusForm;
