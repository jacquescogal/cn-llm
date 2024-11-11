import { useEffect, useState } from "react";
import { WordDTO } from '../types/dto';
import { getWordListBySearch } from "../services/word-api";
import Card from "../components/Card";

const Home = () => {
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [wordList, setWordList] = useState<WordDTO[] | null>(null);

    useEffect(()=>{
        const getWord = async (searchQuery: string) => {
            try{
                const results = await getWordListBySearch(searchQuery, {last_id: 0, limit: 50, has_more: true});
                setWordList(results.word_list);
            } catch(e){
                console.error(e);
                setWordList(null);
            }
        }
        getWord(searchQuery);
    },[searchQuery])
  return (
    <div className="bg-white h-screen w-screen fixed top-0 left-0">
        <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="w-1/2 h-10 rounded-lg border-2 border-black" />
        <div className="grid grid-cols-5">
        {
            wordList && wordList.length?wordList.map((word, index) => (
                <Card key={index} word={word} searchQuery={searchQuery}/>
            )):<h1 className="text-base-content">No results</h1>
        }
        </div>
    </div>
  )
}

export default Home