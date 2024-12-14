import { motion } from "motion/react";
import { useRef, useState } from "react";

import { useSearchContext } from "../context/SearchContext";

export const SearchBar = () => {
  const { searchQuery, setSearchQuery, setIsSearching, setResults } =
    useSearchContext();
  const [focused, setFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const handleSearch = async () => {
    setIsSearching(true);
    inputRef.current?.blur();
    try {
      const data = await fetch(
        `https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?size=10&from
        =0
        &_fulltext=${searchQuery}`
      );
      const response = await data.json();
      console.log("response", response);
      // setResults(response.trials);
    } catch (error) {
      console.error(error);
    } finally {
      setIsSearching(false);
    }
  };
  return (
    <motion.div
      className="flex items-center justify-center h-12 border-2 border-black overflow-hidden"
      initial={{ y: 100, opacity: 0 }}
      animate={{
        borderRadius: focused ? "0px" : "18px",
        y: 0,
        opacity: 1,
      }}
    >
      <input
        ref={inputRef}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && searchQuery) {
            handleSearch();
          }
        }}
        type="text"
        value={searchQuery}
        onChange={(e) => {
          console.log("searchQuery", e.target.value);
          setSearchQuery(e.target.value);
        }}
        placeholder="Describe your condition..."
        className="w-full px-2 rounded-l-lg focus:outline-none font-bold text-xl"
      />
      <button
        className="h-full bg-yellow-400 text-black font-bold m-0 px-2 hover:bg-yellow-500 focus:outline-none
         disabled:hover:bg-yellow-400"
        disabled={!searchQuery}
        onClick={handleSearch}
      >
        Search
      </button>
    </motion.div>
  );
};
