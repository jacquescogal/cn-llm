import Modal from '../modal/Modal'
import ReviewForm from '../forms/ReviewForm'
import { CardType, ReviewDTO, ReviewType } from '../../types/dto';
import { useState } from 'react';
import { getReviewCardById } from '../../services/review-api';


const TestPage = () => {
    const [currentCard, setCurrentCard] = useState<ReviewDTO | null>(null);

    const loadCard = async (card_id: number) =>{
        const card: ReviewDTO = await getReviewCardById(card_id);
        console.log(card)
        setCurrentCard(card);
    }
  return (
    <div>
        <div>Load Choose </div>
        <div className='flex flex-row'>
        <div onClick={()=>{loadCard(1)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - OpenEnded</div>
        <div onClick={()=>{loadCard(2)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - MCQ</div>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - DD</div> */}
        </div>
        <div className='flex flex-row'>
        <div onClick={()=>{loadCard(3)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - OpenEnded</div>
        <div onClick={()=>{loadCard(4)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - MCQ</div>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - DD</div> */}
        </div>
        <div className='flex flex-row'>
        <div onClick={()=>{loadCard(5)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - MCQ</div>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - OCR</div>
        <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - DD</div> */}
        </div>
        <div className='flex flex-row'>
        <div onClick={()=>{loadCard(6)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Tone - MCQ</div>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Tone - DD</div> */}
        </div>
        <div className='flex flex-row'>
        <div onClick={()=>{loadCard(6)}} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Short - MCQ</div>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - OCR</div>
        <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - DD</div> */}
        </div>
        <div className='flex flex-row'>
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - OpenEnded</div> */}
        <div onClick={()=>{
          setCurrentCard(
            {
              card: {
                card_id: 7,
                card_type: CardType.PARAGRAPH,
                review_type: ReviewType.DRAG_AND_DROP,
                fsrs: {
                  due: new Date(),
                  stability: 1,
                  difficulty: 1,
                  elapsed_days: 1,
                  scheduled_days: 1,
                  reps: 1,
                  lapses: 1,
                  state: 1,
                  last_review: new Date(),
                },
                is_disabled: false,
              },
                question: "有一天，小明在公园遇到了他的好朋友。他微笑着说：“%，今天过得怎么样？”朋友回答：“很好，谢谢你，%的关心。”到了晚上，他们要分别了，小明说：“%，希望明天还能见到你。”朋友也挥手说：“%，%你今天的陪伴。”",
                options: ["你好", "我爱你", "再见"]
  
            }
          )
        }} className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - DD</div>
        </div>
        
        <div className='flex flex-row'>
        {currentCard && <Modal modalId='a' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>{currentCard.card.card_type} - {currentCard.card.review_type}</div>} form={<ReviewForm
        reviewDTO={currentCard}/> }/>}
        </div>
    </div>
  )
}

export default TestPage