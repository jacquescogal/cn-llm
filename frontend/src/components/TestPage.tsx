import Modal from './modal/Modal'
import ReviewForm from './forms/ReviewForm'
import { ReviewDTO } from '../types/dto';
import { useState } from 'react';
import { getReviewCardById } from '../services/review-api';


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
        {/* <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - OpenEnded</div>
        <div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - DD</div> */}
        </div>
        
        <div className='flex flex-row'>
        {currentCard && <Modal modalId='a' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>{currentCard.card.card_type} - {currentCard.card.review_type}</div>} form={<ReviewForm
        reviewDTO={currentCard}/> }/>}
        </div>
    </div>
  )
}

export default TestPage