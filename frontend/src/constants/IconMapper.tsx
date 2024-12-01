import { MdOutlineQuestionMark } from "react-icons/md";
import { CardType } from "../types/dto";
import { RiPinyinInput } from "react-icons/ri";
import { FaMicrophone, FaParagraph } from "react-icons/fa";

export const  CardTypeIconMap= ({cardType}: { cardType: CardType; })=> {
    return (
        <>
        {
            cardType === CardType.Meaning && <MdOutlineQuestionMark/>
        }
        {
            cardType === CardType.Pinyin && <RiPinyinInput/>
        }
        {
            cardType === CardType.Hanzi && "中"
        }
        {
            cardType === CardType.TONE && <FaMicrophone/>
        }
        {
            cardType === CardType.PARAGRAPH && <FaParagraph/>
        }
        </>
    )
}
