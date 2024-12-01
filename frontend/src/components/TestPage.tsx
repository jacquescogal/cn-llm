import Modal from './common/modal/Modal'
import ReviewForm from './common/forms/ReviewForm'
import { CardType, ReviewType } from '../types/dto'


const TestPage = () => {
  return (
    <div>
        <div className='flex flex-row'>
        <Modal modalId='a' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - OpenEnded</div>} form={<ReviewForm 
        card_id={1}
        card_type={CardType.Meaning}
        review_type={ReviewType.OpenEnded}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='b' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - MCQ</div>} form={<ReviewForm
        card_id={2}
        card_type={CardType.Meaning}
        review_type={ReviewType.MCQ}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='c' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Meaning - DD</div>} form={<ReviewForm
        card_id={3}
        card_type={CardType.Meaning}
        review_type={ReviewType.DRAG_AND_DROP}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        </div>
        <div className='flex flex-row'>
        <Modal modalId='d' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - OpenEnded</div>} form={<ReviewForm
        card_id={4}
        card_type={CardType.Pinyin}
        review_type={ReviewType.OpenEnded}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='e' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - MCQ</div>} form={<ReviewForm
        card_id={5}
        card_type={CardType.Pinyin}
        review_type={ReviewType.MCQ}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='f' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Pinyin - DD</div>} form={<ReviewForm
        card_id={6}
        card_type={CardType.Pinyin}
        review_type={ReviewType.DRAG_AND_DROP}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        </div>
        <div className='flex flex-row'>
        <Modal modalId='g' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - MCQ</div>} form={<ReviewForm
        card_id={7}
        card_type={CardType.Hanzi}
        review_type={ReviewType.MCQ}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='h' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - OCR</div>} form={<ReviewForm
        card_id={8}
        card_type={CardType.Hanzi}
        review_type={ReviewType.OCR}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='i' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Hanzi - DD</div>} form={<ReviewForm
        card_id={1}
        card_type={CardType.Hanzi}
        review_type={ReviewType.DRAG_AND_DROP}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        </div>
        <div className='flex flex-row'>
        <Modal modalId='j' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Tone - MCQ</div>} form={<ReviewForm
        card_id={1}
        card_type={CardType.TONE}
        review_type={ReviewType.MCQ}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='k' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Tone - DD</div>} form={<ReviewForm
        card_id={1}
        card_type={CardType.TONE}
        review_type={ReviewType.DRAG_AND_DROP}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        </div>
        <div className='flex flex-row'>
        <Modal modalId='l' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - OpenEnded</div>} form={<ReviewForm
        card_id={1}
        card_type={CardType.PARAGRAPH}
        review_type={ReviewType.OpenEnded}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        <Modal modalId='m' reactNode={<div className='bg-slate-100 h-24 w-48 cursor-pointer m-4'>Paragraph - DD</div>} form={<ReviewForm
        card_id={1}
        card_type={CardType.PARAGRAPH}
        review_type={ReviewType.DRAG_AND_DROP}
        card_content_json='{"question":"What is the meaning of this word?","answer":"This is the answer"}'
        />}/>
        </div>
    </div>
  )
}

export default TestPage