library(tm)
library(data.table)
library(stringr)

f <- file("stdin")
on.exit(close(f))

x <- readLines(f)

corpus <- readLines("corpus.txt",skipNul = TRUE, warn = TRUE)

sample_size = 2000 #max sample size allowed by hackkerank due to memory limits

# make a random sample
sample_data <- corpus[sample(1:length(corpus),sample_size)]

# cleaning the sample
mycorpus<-VCorpus(VectorSource(sample_data))
mycorpus <- tm_map(mycorpus, content_transformer(tolower)) # convert to lowercase
mycorpus <- tm_map(mycorpus, removePunctuation) # remove punctuation
mycorpus <- tm_map(mycorpus, removeNumbers) # remove numbers
mycorpus <- tm_map(mycorpus, stripWhitespace) # remove multiple whitespace
changetospace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
mycorpus <- tm_map(mycorpus, changetospace, "/|@|\\|")

# making a TDM
oneGM <- TermDocumentMatrix(mycorpus)

freqTerms1 <- findFreqTerms(oneGM, lowfreq = 1)
termFreq1 <- as.matrix(oneGM[freqTerms1,])
#vector of possible solutions
soln = c("is","are","were","am","been","was","being","be")
text = x[2]
#processing the input
text <- str_split_fixed(text,'----',n=Inf)
text <- str_squish(text)

# Check if a list contains an index or not
Element_Exists_Check = function( full_index_path ){
  tryCatch({
    len_element = length(full_index_path)
    exists_indicator = ifelse(len_element > 0, T, F)
    return(exists_indicator)
  }, error = function(e) {
    return(F)
  })
}
#finding the last word before ---- in inputs
text <- word(text,-1)
cd <- 0
y<-as.integer(x[1])
for (j in 1:y){
  
  for (i in 1:length(soln)){
  if (!Element_Exists_Check(termFreq1[soln[i],]) ||!Element_Exists_Check(termFreq1[text[j],]) )
  {  #Data Not exists in our model. Assign some random value <0.05
      cd[i] <- runif(1,max=0.2)
     }
    else
#finding and storing the correlations between one word before ---- and the 8 possible solutions
    cd[i]<- cor(termFreq1[j,], termFreq1[soln[i],])
  }

  cat(soln[which.max(cd)],sep='\n')
  }

