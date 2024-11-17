import { useEffect, useRef, useState } from "react";
import { HSKLevel, PageMetaDTO, WordDTO, WordSearchFilter } from "../../types/dto";
import { getWordList, getWordListBySearch } from "../../services/word-api";
import ExploreCard from "./ExploreCard";
import SearchBar from "./SearchBar";

interface FilterCheck {
  label: string;
  value: number;
  checked: boolean;
  indeterminate: boolean;
}

const ExplorePage = () => {
  const pageMetaDTORef = useRef<PageMetaDTO>({
    offset: 0,
    limit: 50,
    has_more: true,
  });

  const resetPageMetaDTO = () => {
    pageMetaDTORef.current = {
      offset: 0,
      limit: 50,
      has_more: true,
    };
  }
  const [hskFilters, setHskFiltersState] = useState<FilterCheck[]>(
    Array({
      label: "All",
      value: 0,
      checked: true,
      indeterminate: false,
    }).concat(
      Array.from(
        {
          length: Object.keys(HSKLevel).filter((key) => isNaN(Number(key)))
            .length,
        },
        (_, i) => ({
          label: `HSK ${i + 1}`,
          value: i + 1,
          checked: true,
          indeterminate: false,
        })
      )
    )
  );
  const hskFiltersRef = useRef(hskFilters);
  const setHskFilters = (value: FilterCheck[]) => {
    hskFiltersRef.current = value;
    setHskFiltersState(value);
  }
  const [learntFilters, setLearntFiltersState] = useState<FilterCheck[]>(
    Array({
      label: "Both",
      value: 0,
      checked: true,
      indeterminate: false,
    }).concat(
      Array.from({ length: 2 }, (_, i) => ({
        label: i === 0 ? "Learnt" : "Not Learnt",
        value: i + 1,
        checked: true,
        indeterminate: false,
      }))
    )
  );
  const learntFiltersRef = useRef(learntFilters);
  const setLearntFilters = (value: FilterCheck[]) => {
    learntFiltersRef.current = value;
    setLearntFiltersState(value);
  }
  const [searchQuery, setSearchQueryState] = useState<string>("");
  const searchQueryRef = useRef<string>(searchQuery);
  const setSearchQuery = (value: string) => {
    searchQueryRef.current = value;
    setSearchQueryState(value);
  }

  const [wordList, setWordList] = useState<WordDTO[] | null>(null);

  const selectHSKLevel = (level: number) => {
    const currentLevel = hskFilters.find(
      (hskFilter) => hskFilter.value === level
    );
    if (level === 0 && currentLevel?.indeterminate) {
      const newHskFilters = hskFilters.map((hskFilter) => {
        return {
          ...hskFilter,
          checked: true,
          indeterminate: false,
        };
      });
      setHskFilters(newHskFilters);
      return;
    } else if (level === 0 && !currentLevel?.indeterminate) {
      if (currentLevel?.checked) {
        const newHskFilters = hskFilters.map((hskFilter) => {
          return {
            ...hskFilter,
            checked: false,
            indeterminate: false,
          };
        });
        setHskFilters(newHskFilters);
        return;
      } else {
        const newHskFilters = hskFilters.map((hskFilter) => {
          return {
            ...hskFilter,
            checked: true,
            indeterminate: false,
          };
        });
        setHskFilters(newHskFilters);
        return;
      }
    }
    const updatedHskFilters = hskFilters.map((hskFilter) => {
      if (hskFilter.value === level) {
        return {
          ...hskFilter,
          checked: !hskFilter.checked,
        };
      }
      return hskFilter;
    });
    const countChecked = updatedHskFilters.filter(
      (hskFilter) => hskFilter.checked && hskFilter.value !== 0
    ).length;
    const newAllLevel = hskFilters.find((hskFilter) => hskFilter.value === 0);
    newAllLevel!.indeterminate =
      countChecked > 0 && countChecked < hskFilters.length - 1;
    const newHskFilters = updatedHskFilters.map((hskFilter) => {
      if (hskFilter.value === 0) {
        return {
          ...hskFilter,
          checked: countChecked === hskFilters.length - 1,
          indeterminate: newAllLevel!.indeterminate,
        };
      }
      return hskFilter;
    });
    setHskFilters(newHskFilters);
  };
  const selectLearnt = (value: number) => {
    const currentLevel = learntFilters.find(
      (learntFilter) => learntFilter.value === value
    );
    console.log(currentLevel);
    if (value === 0 && currentLevel?.indeterminate) {
      const newLearntFilters = learntFilters.map((learntFilter) => {
        return {
          ...learntFilter,
          checked: true,
          indeterminate: false,
        };
      });
      setLearntFilters(newLearntFilters);
      return;
    } else if (value === 0 && !currentLevel?.indeterminate) {
      if (currentLevel?.checked) {
        const newLearntFilters = learntFilters.map((learntFilter) => {
          return {
            ...learntFilter,
            checked: false,
            indeterminate: false,
          };
        });
        setLearntFilters(newLearntFilters);
        return;
      } else {
        const newLearntFilters = learntFilters.map((learntFilter) => {
          return {
            ...learntFilter,
            checked: true,
            indeterminate: false,
          };
        });
        setLearntFilters(newLearntFilters);
        return;
      }
    }
    const updatedLearntFilters = learntFilters.map((learntFilter) => {
      if (learntFilter.value === value) {
        return {
          ...learntFilter,
          checked: !learntFilter.checked,
        };
      }
      return learntFilter;
    });
    const countChecked = updatedLearntFilters.filter(
      (learntFilter) => learntFilter.checked && learntFilter.value !== 0
    ).length;
    const newAllLevel = learntFilters.find(
      (learntFilter) => learntFilter.value === 0
    );
    newAllLevel!.indeterminate =
      countChecked > 0 && countChecked < learntFilters.length - 1;
    const newLearntFilters = updatedLearntFilters.map((learntFilter) => {
      if (learntFilter.value === 0) {
        return {
          ...learntFilter,
          checked: countChecked === learntFilters.length - 1,
          indeterminate: newAllLevel!.indeterminate,
        };
      }
      return learntFilter;
    });
    setLearntFilters(newLearntFilters);
  };

  const getWord = async () => {
    const currentOffset = pageMetaDTORef.current.offset;
    const hskFilters = hskFiltersRef.current;
    const learntFilters = learntFiltersRef.current;
    if (
      hskFilters.every((hskFilter) => !hskFilter.checked) ||
      learntFilters.every((learntFilter) => !learntFilter.checked)
    ) {
      setWordList(null);
      return;
    }
    const wordSearchFilter: WordSearchFilter = {};
    const hskList = hskFilters
      .filter((hskFilter) => hskFilter.checked && hskFilter.value !== 0)
      .map((hskFilter) => hskFilter.value);
    if (hskList.length > 0) {
      wordSearchFilter.hsk = hskList;
    }
    const learntList = learntFilters
      .filter(
        (learntFilter) => learntFilter.checked && learntFilter.value !== 0
      )
      .map((learntFilter) => learntFilter.value);
    if (learntList.length == 1) {
      wordSearchFilter.learnt = learntList[0] === 1;
    }
    if (searchQueryRef.current.length < 1) {
      try {
        const results = await getWordList(
          pageMetaDTORef.current
          ,
          wordSearchFilter
        );
        if (currentOffset !== pageMetaDTORef.current.offset){
          return;
        }
        if (pageMetaDTORef.current.offset > 0) {
          setWordList((prevWordList) => {
            if (prevWordList) {
              return prevWordList.concat(results.word_list);
            }
            return results.word_list;
          });
        }else{
          setWordList(results.word_list);
        }
        pageMetaDTORef.current = results.page_meta;
      } catch (e) {
        console.error(e);
        setWordList(null);
        resetPageMetaDTO();
      }
    } else {
      try {
        console.log("searching keyword")
        const results = await getWordListBySearch(searchQueryRef.current, pageMetaDTORef.current
          ,
          wordSearchFilter);
        if (pageMetaDTORef.current.offset > 0) {
          setWordList((prevWordList) => {
            if (prevWordList) {
              return prevWordList.concat(results.word_list);
            }
            return results.word_list;
          });
        }else{
          setWordList(results.word_list);
        }
        pageMetaDTORef.current = results.page_meta;
      } catch (e) {
        console.error(e);
        setWordList(null);
        resetPageMetaDTO();
      }
    }
  };
  useEffect(() => {
    resetPageMetaDTO();
    getWord();
    if (containerRef.current) {
      containerRef.current.scrollTop = 0;
    }
  }, [searchQuery, hskFilters, learntFilters]);
  const containerRef = useRef<HTMLDivElement>(null);
  const handleScroll = () => {
    const element = containerRef.current;
    if (element) {
      const { scrollTop, scrollHeight, clientHeight } = element;
      if (scrollTop + clientHeight >= scrollHeight-100) {
        handleReachBottom();
      }
    }
  };

  const handleReachBottom = () => {
    if (!pageMetaDTORef.current.has_more) {
      return;
    }
    getWord();
  };

  useEffect(() => {
    const element = containerRef.current;
    if (element) {
      element.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (element) {
        element.removeEventListener("scroll", handleScroll);
      }
    };
  }, []);
  return (
    <div className="relative h-full bg-inherit flex flex-col">
        <div className="flex flex-row justify-center py-2 ">
          <FilterDropdown
            label={"HSK Filter"}
            filters={hskFilters}
            selectFilterValue={selectHSKLevel}
          />
          <FilterDropdown
            label={"Learnt Filter"}
            filters={learntFilters}
            selectFilterValue={selectLearnt}
          />
          <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
        </div>
        <div ref={containerRef} className="grid grid-cols-2 lg:grid-cols-3 2xl:grid-cols-5 bg-base-100 h-full m-4 p-4 gap-y-2 overflow-y-scroll justify-items-center rounded-xl shadow-md">
          {wordList && wordList.length ? (
            wordList.map((word, index) => (
              <ExploreCard key={index} word={word} searchQuery={searchQuery} />
            ))
          ) : (
            <h1 className="text-base-content">No results</h1>
          )}
        </div>
      </div>
    );
};

const FilterDropdown = ({
  label,
  filters,
  selectFilterValue,
}: {
  label: string;
  filters: FilterCheck[];
  selectFilterValue: (value: number) => void;
}) => {
  return (
    <div className="form-control">
      <div className="dropdown">
        <div tabIndex={0} role="button" className="btn mx-1">
          {label}
        </div>
        <ul
          tabIndex={0}
          className="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow"
        >
          {filters.map((filter, index) => (
            <li key={index}>
              <FilterCheckBoxOption
                filter={filter}
                selectFilterValue={selectFilterValue}
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

type HTMLElementWithIndeterminate = HTMLElement & { indeterminate: boolean };

const FilterCheckBoxOption = ({
  filter,
  selectFilterValue,
}: {
  filter: FilterCheck;
  selectFilterValue: (value: number) => void;
}) => {
  useEffect(() => {
    (
      document.getElementById(filter.label)! as HTMLElementWithIndeterminate
    ).indeterminate = filter.indeterminate;
  }, [filter.indeterminate, filter.label]);
  return (
    <label className="label cursor-pointer">
      <span className="label-text">{filter.label}</span>
      <input
        id={filter.label}
        type="checkbox"
        className="checkbox absolute right-0"
        onChange={() => {
          selectFilterValue(filter.value);
        }}
        checked={filter.checked}
      />
    </label>
  );
};

export default ExplorePage;
