BstEvad <- read.csv("BstEvad_v2.csv")
BstPurs <- read.csv("BstPur_v2.csv")

ne <- nrow(BstEvad) # 90
np <- nrow(BstPurs) # 90

SIZETEAMS <- 2 # 2 or 3

numTeams2Players <- 30


if (SIZETEAMS == 2) {
  BstEvad <- BstEvad[1:numTeams2Players,]  # Only for teams with two players
  BstPurs <- BstPurs[1:numTeams2Players,]  # Only for teams with two players
  num <- numTeams2Players # 30
  ADDINC <- 0
} else {
  BstEvad <- BstEvad[(numTeams2Players+1):ne,]  # Only for teams with two players
  BstPurs <- BstPurs[(numTeams2Players+1):np,]  # Only for teams with two players
  num <- ne - numTeams2Players # 60
  ADDINC <- numTeams2Players
}

cumRglobal <- 0
maxRglobal <- -Inf
minRglobal <- +Inf

WHOSTARTS <- "pursuer" # "pursuer" or "evader"
nrep <- 20
# set.seed(0)
#pursChoice <- 1
#pursChoice <- sample(numTeams2Players, 1)
for (k in 1:num) {
  cat(paste0("\n\nLine-up start:", k, "\n"))
  if (WHOSTARTS == "pursuer") {
    pursChoice <- k
    evadChoice <- -1
  } else {
    pursChoice <- -1
    evadChoice <- k
  }  
  
  cumR <- 0
  countR <- 0
  
  for (i in 1:nrep) {
    if ((WHOSTARTS == "pursuer") || (i > 1)) {
      Md <- BstEvad[pursChoice,]$Md
      Dd <- BstEvad[pursChoice,]$Dd
      Ld <- BstEvad[pursChoice,]$Ld
      Rd <- BstEvad[pursChoice,]$Rd
      Ad <- BstEvad[pursChoice,]$Ad
      cat(paste0("Pursuer #", pursChoice + ADDINC, " (", Md, Dd, Ld, Rd, "|", Ad, ")."))
      Mr <- BstEvad[pursChoice,]$Mr
      Dr <- BstEvad[pursChoice,]$Dr
      Lr <- BstEvad[pursChoice,]$Lr
      Rr <- BstEvad[pursChoice,]$Rr
      Ar <- BstEvad[pursChoice,]$Ar
      R1 <- BstEvad[pursChoice,]$R
      cumR <- cumR + R1
      countR <- countR + 1
      cat(paste0("   Best Evader: (", Mr, Dr, Lr, Rr, "|", Ar, ") with reward: ", R1))
      for (j in 1:num) {
        if ((BstPurs[j,]$Mr == Mr) &&
            (BstPurs[j,]$Dr == Dr) &&
            (BstPurs[j,]$Lr == Lr) &&
            (BstPurs[j,]$Rr == Rr) && 
            (BstPurs[j,]$Ar == Ar)) {
          evadChoiceNew <- j
          break
        }  
      }
      if (evadChoice == evadChoiceNew) {
        cat("  Convergence!\n")
        # uncomment these lines to calculate the exact result in the limit when there's convergence
        # cumR <- R1
        # countR <- 1
        #  break
      } else {
        cat("\n")
        evadChoice = evadChoiceNew
      }  
    }
    
    Mr <- BstPurs[evadChoice,]$Mr
    Dr <- BstPurs[evadChoice,]$Dr
    Lr <- BstPurs[evadChoice,]$Lr
    Rr <- BstPurs[evadChoice,]$Rr
    Ar <- BstPurs[evadChoice,]$Ar    
    cat(paste0("Evader  #", evadChoice + ADDINC, " (", Mr, Dr, Lr, Rr, "|", Ar, ")."))
    Md <- BstPurs[evadChoice,]$Md
    Dd <- BstPurs[evadChoice,]$Dd
    Ld <- BstPurs[evadChoice,]$Ld
    Rd <- BstPurs[evadChoice,]$Rd
    Ad <- BstPurs[evadChoice,]$Ad
    R2 <- BstPurs[evadChoice,]$R 
    cumR <- cumR + R2
    countR <- countR + 1
    cat(paste0("  Best Pursuer: (", Md, Dd, Ld, Rd, "|", Ad, ") with reward: ", R2, "\n"))
    for (j in 1:num) {
      if ((BstEvad[j,]$Md == Md) &&
          (BstEvad[j,]$Dd == Dd) &&
          (BstEvad[j,]$Ld == Ld) &&
          (BstEvad[j,]$Rd == Rd) && 
          (BstEvad[j,]$Ad == Ad)) {
        pursChoice <- j
        break
      }  
    }
  }
  cat("\n")
  avgR <- cumR/(1.0*countR)
  cat(paste0("Average R: ", avgR, "\n"))
  
  cumRglobal <- cumRglobal + avgR
  if (maxRglobal < avgR)
    maxRglobal <- avgR
  if (minRglobal > avgR)
    minRglobal <- avgR
  
  cat(paste0("\nEnd of"), num, "initial teams. Mean R: ", cumRglobal/num, ", Max R: ", maxRglobal, ", Min R: ", minRglobal, "\n")
  
}



