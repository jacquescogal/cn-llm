import { useEffect, useRef, useState } from "react";
import { CardType, ReviewDTO, ReviewType } from "../../types/dto";

const ReviewForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  return (
    <div className="w-full h-full flex flex-col  items-center">
      {props.reviewDTO.card.card_type === CardType.Meaning && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.OpenEnded &&
            ReviewMeaningOpenEndedForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.MCQ &&
            ReviewMeaningMCQForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.DRAG_AND_DROP &&
            "Meaning Drag and Drop"}
        </>
      )}

      {props.reviewDTO.card.card_type === CardType.Pinyin && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.OpenEnded &&
            ReviewPinyinOpenEndedForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.MCQ &&
            ReviewPinyinMCQForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.DRAG_AND_DROP &&
            "Meaning Drag and Drop"}
        </>
      )}

      {props.reviewDTO.card.card_type === CardType.Hanzi && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.MCQ &&
            ReviewHanziMCQForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.DRAG_AND_DROP &&
            "Meaning Drag and Drop"}
        </>
      )}

      {props.reviewDTO.card.card_type === CardType.TONE && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.MCQ &&
            ReviewToneMCQForm({ reviewDTO })}
          {props.reviewDTO.card.review_type === ReviewType.DRAG_AND_DROP &&
            "Meaning Drag and Drop"}
        </>
      )}

      {props.reviewDTO.card.card_type === CardType.PARAGRAPH && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.DRAG_AND_DROP &&
            ReviewParaDndForm({ reviewDTO })}
        </>
      )}

      {props.reviewDTO.card.card_type === CardType.SHORT_PARAGRAPH && (
        <>
          {props.reviewDTO.card.review_type === ReviewType.MCQ &&
            ReviewShortMCQForm({ reviewDTO })}
        </>
      )}
    </div>
  );
};

const ReviewMeaningOpenEndedForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (e.target.value.length <= 200) {
      setAttempt(e.target.value);
      bottomRef?.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1 className="text-3xl">{reviewDTO?.pinyin}</h1>
        <h1 className="text-md border border-2 border-dashed border-black bg-gray-100 rounded-sm shodow-inner w-40 h-16 my-4 p-1 overflow-y-auto break-all">
          {attempt}
          <div ref={bottomRef}></div>
        </h1>
      </div>
      <label className="form-control">
        <div className="label">
          <span className="label-text">Answer:</span>
          <span className="label-text-alt">
            {200 - attempt.length} characters left
          </span>
        </div>
        <textarea
          className="textarea textarea-bordered w-96 h-40"
          style={{ resize: "none" }}
          placeholder="Type here"
          onChange={handleInput}
          value={attempt}
        />
        <button className="absolute right-4 bottom-4 bg-black-100 border border-black border-rounded rounded-md py-1 px-4 m-2 text-base-content text-center select-none mt-4 bg-white hover:bg-black hover:text-white">
          Next
        </button>
      </label>
    </>
  );
};

const ReviewMeaningMCQForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1 className="text-3xl">{reviewDTO?.pinyin}</h1>
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-16 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt}
          <div ref={bottomRef}></div>
        </h1>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

const ReviewPinyinOpenEndedForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);
  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-16 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt}
          <div ref={bottomRef}></div>
        </h1>
        <h1 className="text-3xl">{reviewDTO?.meaning}</h1>
      </div>
      <label className="form-control">
        <div className="label">
          <span className="label-text">Answer:</span>
          <span className="label-text-alt">200 characters left</span>
        </div>
        <textarea
          className="textarea textarea-bordered w-96 h-40"
          style={{ resize: "none" }}
          placeholder="Type here"
          onChange={(e) => {
            setAttempt(e.target.value);
            bottomRef?.current?.scrollIntoView({ behavior: "smooth" });
          }}
        />
        <button className="absolute right-4 bottom-4 bg-black-100 border border-black border-rounded rounded-md py-1 px-4 m-2 text-base-content text-center select-none mt-4 bg-white hover:bg-black hover:text-white">
          Next
        </button>
      </label>
    </>
  );
};

const ReviewPinyinMCQForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-16 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt}
          <div ref={bottomRef}></div>
        </h1>
        <h1 className="text-3xl">{reviewDTO?.meaning}</h1>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer select-none w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

const ReviewHanziMCQForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-12 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt}
          <div ref={bottomRef}></div>
        </h1>
        <h1 className="text-3xl">{reviewDTO?.pinyin}</h1>
        <h1 className="text-3xl">{reviewDTO?.meaning}</h1>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer select-none w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

const ReviewToneMCQForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-72 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-12 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt.length === 0 ? reviewDTO?.toneless_pinyin : attempt}
          <div ref={bottomRef}></div>
        </h1>
        <h1 className="text-3xl">{reviewDTO?.pinyin}</h1>
        <h1 className="text-3xl">{reviewDTO?.meaning}</h1>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer select-none w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

const ReviewParaDndForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  return (
    <>
      <div>{reviewDTO.question}</div>
      <div className="relative bg-base-100 h-60 w-96 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
        <h1 className="text-5xl">{reviewDTO?.hanzi}</h1>
        <h1
          className={`text-3xl border border-2 border-dashed border-black  rounded-sm shadow-inner w-40 h-12 my-1 p-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "" : "bg-gray-100"
          }`}
        >
          {attempt.length === 0 ? reviewDTO?.toneless_pinyin : attempt}
          <div ref={bottomRef}></div>
        </h1>
        <h1 className="text-3xl">{reviewDTO?.pinyin}</h1>
        <h1 className="text-3xl">{reviewDTO?.meaning}</h1>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer select-none w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

const ReviewShortMCQForm = (props: { reviewDTO: ReviewDTO }) => {
  const { reviewDTO } = props;
  const [attempt, setAttempt] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAttempt(event.target.value);
  };

  useEffect(() => {
    setAttempt("");
  }, [reviewDTO]);

  const splitSentenceByPercent = (sentence: string): string[] => {
    return sentence.split(/%/);
  };
  return (
    <>
      
      <div className="text-3xl relative bg-base-100 h-60 w-96 flex-0 flex flex-col content-center justify-center items-center border border-2 border-black rounded-md">
      <div className="flex flex-row content-center justify-center items-center ">
        <span>{splitSentenceByPercent(reviewDTO.question)[0]}</span>
        <h1
          className={`border border-2 mx-2  rounded-sm shadow-inner w-12 h-12 py-1 my-1 overflow-y-auto break-all ${
            attempt.length > 0 ? "border-gray-300" : "bg-gray-100 border-dashed border-black "
          }`}
        >
          {attempt.length === 0 ? reviewDTO?.toneless_pinyin : attempt}
          <div ref={bottomRef}></div>
        </h1>
        <span>{splitSentenceByPercent(reviewDTO.question)[1]}</span>
      </div>
      </div>

      {/* radio buttons mcq */}
      <div className="flex flex-col mt-4 space-y-2">
        {reviewDTO.options?.map((option, idx) => (
          <label
            key={idx}
            className={`flex items-center space-x-2 p-2 border rounded-md cursor-pointer select-none w-72 ${
              attempt === option
                ? "bg-blue-100 border-blue-400"
                : "border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="mcq"
              value={option}
              checked={attempt === option}
              onChange={handleOptionChange}
              className="radio radio-primary border-gray-300 checked:bg-blue-500 checked:border-blue-500"
            />
            <span>{option}</span>
          </label>
        ))}
      </div>
    </>
  );
};

export default ReviewForm;
