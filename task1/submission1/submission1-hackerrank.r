library(stringr)
library(tm)

#all possible keys
ks <- c("axe deo","best-seller books","calvin klein","camcorder","camera","chemistry","chromebook","c programming","data structures algorithms","dell laptops","dslr canon","mathematics","nike-deodrant","physics","sony cybershot","spoken english","timex watch","titan watch","tommy watch","written english");
f <- file("stdin")
on.exit(close(f))

x <- readLines(f)
y <- strsplit(x, "\n")
x <- as.numeric(x[[1]])
input = "";

for (i in 1:x){
  
  input[i] <- y[i+1];
  
}
#cleaning the input
input <- tolower(input);
input <- str_replace_all(input, "[^[:alnum:]]", " ")
input <- removeWords(input,stopwords("en"))
input <- str_squish(input)
lst <- array(logical(),c(x,20)) 
score <- replicate(x, 0)
score <- replicate(20,score)

for (i in 1:20){
 lst[,i] <- mapply(grepl, ks[i], input);
}
res <- ""

#finding score for the main string itself
for (i in 1:x){
  
  
  for (j in 1:20){
    
    if (lst[i,j]==TRUE)
      score[i,j] = score[i,j] + 100;
    
  }
  
  
}

#finding score for a substring
for (i in 1:x){
  
  for (j in 1:20){
    
  tokensj <- strsplit(ks[j], split=" ")
  tokensj <- unlist(tokensj, use.names=FALSE)
  truv<-sum(str_detect(input[i], tokensj))
 
 score[i,j] = score[i,j] + 10*truv;   
    
  }
  res[i] <- ks[which.max(score[i,])]
  
}
cat(res,sep='\n')

