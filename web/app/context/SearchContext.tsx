import { createContext, useContext, useState } from "react";

const SearchContext = createContext<{
  searchQuery: string;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
  isSearching: boolean;
  setIsSearching: React.Dispatch<React.SetStateAction<boolean>>;
}>({
  searchQuery: "",
  setSearchQuery: () => {},
  isSearching: false,
  setIsSearching: () => {},
});

export const useSearchContext = () => useContext(SearchContext);

export const SearchContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  return (
    <SearchContext.Provider
      value={{
        searchQuery,
        setSearchQuery,
        isSearching,
        setIsSearching,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};
