import { createContext, useContext, useState } from "react";
import { ClinicalTrial } from "../types/trial";

const SearchContext = createContext<{
  searchQuery: string;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
  isSearching: boolean;
  setIsSearching: React.Dispatch<React.SetStateAction<boolean>>;
  results: ClinicalTrial[];
  setResults: React.Dispatch<React.SetStateAction<ClinicalTrial[]>>;
}>({
  searchQuery: "",
  setSearchQuery: () => {},
  isSearching: false,
  setIsSearching: () => {},
  results: [],
  setResults: () => {},
});

export const useSearchContext = () => useContext(SearchContext);

export const SearchContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<ClinicalTrial[]>([]);
  return (
    <SearchContext.Provider
      value={{
        searchQuery,
        setSearchQuery,
        isSearching,
        setIsSearching,
        results,
        setResults,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};
