import React from "react";
import { WordDTO } from "../types/dto";

const Card = (props: {word:WordDTO, searchQuery: string}) => {
    const word = props.word;
  return (
    <div className="relative bg-base-100 border-black border-4 h-48 w-80 rounded-xl shadow-inset shadow-md">
      <div className="absolute left-2 top-2">
        <h1 className="text-base-content text-xs select-none">
          {word.hsk_level}:{word.word_id}
        </h1>
      </div>

      <div className="w-full h-full flex justify-center  items-center mt-2">
        <div className="flex flex-col">
          <h1 className="text-base-content text-7xl">{word.hanzi}</h1>
          <span className="text-base-content text-md">{highLight(word.pinyin, props.searchQuery)}</span>
        </div>
      </div>
    </div>
  );
};

const highLight = (word: string, searchQuery: string) =>{
    const index = removePinyinTones(word).indexOf(searchQuery);
    if(index === -1){
        return word;
    }
    return (
        <>
            {word.slice(0, index)}
            <span className="bg-primary">{word.slice(index, index + searchQuery.length)}</span>
            {word.slice(index + searchQuery.length)}
        </>
    )
}
function removePinyinTones(pinyin: string): string {
    const toneMap: { [key: string]: string } = {
      'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
      'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e',
      'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
      'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
      'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
      'ǖ': 'u', 'ǘ': 'u', 'ǚ': 'u', 'ǜ': 'u',
      'ü': 'u', 'ń': 'n', 'ň': 'n', '': 'm'
    };
  
    return pinyin.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüńň]/g, (match) => toneMap[match] || match);
  }
    

export default Card;
