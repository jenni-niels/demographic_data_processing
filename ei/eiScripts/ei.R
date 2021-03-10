suppressMessages(library(tidyverse))
suppressMessages(library(eiPack))
suppressMessages(library(rgdal))
suppressMessages(library(foreign))
suppressMessages(library(readr))
suppressMessages(library(optparse))
suppressMessages(library(parallel))


args <- commandArgs(trailingOnly=TRUE)

run_ei <- function(args, j) {

  options(readr.num_columns = 0)

  data_run <- args[1]
  bufferCol <- args[2] == "buffer"
  scaleVotes <- args[2] == "scaleVotes"
  scalePop <- args[2] == "scalePop"


  # print alphas, betas, and counts, but for betas do a subset of the precincts

  ntunes_val <- 100
  tunedraws <- 1000
  burnin_mcmc <- strtoi(args[3])
  thin_mcmc <- strtoi(args[4])
  sample_mcmc <- strtoi(args[5])

  total_run_length <- burnin_mcmc + (thin_mcmc * sample_mcmc)

  ei_run <- paste("EI", args[2], burnin_mcmc, thin_mcmc, sample_mcmc, sep="_")
  wd <- getwd()
  # data_dir <- paste("../../shapes/AZ_vtds/", data_run, ".shp", sep="")
  data_dir <- paste("../../shapes/GA_precincts/", data_run, "/", data_run, ".shp", sep="")
  # data_dir <- paste("../../shapes/WI_2020_ward_groups/", data_run, "/", data_run, ".shp", sep="")
  data <- readOGR(dsn=data_dir, verbose=FALSE)
  data <- as(data, "data.frame")
  output_dir <- paste(wd, "../outputs", data_run, ei_run, j, sep="/")
  dir.create(output_dir, recursive=TRUE)

  print(paste("Saving EI results to ../outputs", data_run, ei_run, j, sep="/"))

  data$OCVAP <- 0 # VAP!?
  data$OCVAP <- as.numeric(data$CVAP) - as.numeric(data$AMINCVAP.) # VAP!?
  demographics <- c('AMINCVAP.', 'OCVAP') # VAP!?
  candidates <- c('PRES20D', 'PRES20R')
  cols <- c(demographics, candidates)

  # print(sum(as.numeric(data$PRES20D)) - sum(as.numeric(data$PRES20R)))
  data <- data[complete.cases(data),] # remove nan rows
  # print(sum(as.numeric(data$PRES20D)) - sum(as.numeric(data$PRES20R)))
  for (col in cols) { # round to Ints
    data[[col]] <- as.numeric(data[[col]])
    data[[col]] <- round(data[[col]], digits=0)
  }

  data$TOTPOP <- rowSums(data[,demographics])
  data$TOTVOTES <- rowSums(data[,candidates])
  data <- data[data$TOTPOP > 0,] # remove zero-population precincts

  # handle POP < totvotes cases differently...
  if (bufferCol) {
    # add a buffer POP column
    demographics <- append(demographics, "bufferPOP")
    data$bufferPOP <- 0
    data$bufferPOP[data$TOTPOP < data$TOTVOTES] <- data$TOTVOTES[data$TOTPOP < data$TOTVOTES] - data$TOTPOP[data$TOTPOP < data$TOTVOTES]
    data$TOTPOP <- rowSums(data[,demographics])
  } else if (scaleVotes) {
    # or scale votes DOWN to match POP
    data$factor <- 1
    data$factor[data$TOTPOP < data$TOTVOTES] <- data$TOTPOP[data$TOTPOP < data$TOTVOTES] / data$TOTVOTES[data$TOTPOP < data$TOTVOTES]
    for (candidate in candidates) {
      data[[candidate]] <- floor(data[[candidate]] * data$factor)
    }
    data$TOTVOTES <- rowSums(data[,candidates])
  } else if (scalePop) {
    # or scale POP UP to match votes
    data$factor <- 1
    data$factor[data$TOTPOP < data$TOTVOTES] <- data$TOTVOTES[data$TOTPOP < data$TOTVOTES] / data$TOTPOP[data$TOTPOP < data$TOTVOTES]
    for (group in demographics) {
      data[[group]] <- ceiling(data[[group]] * data$factor)
    }
    data$TOTPOP <- rowSums(data[,demographics])
  } else {
    print("ERROR! You need to specify 'buffer', 'scaleVotes', or 'scalePop'")
    break
  }

  data$NOTVOTES <- data$TOTPOP - data$TOTVOTES
  candidates <- c(candidates, "NOTVOTES")

  # identify formula: estimate vote/no vote for black, hisp, and other
  candidates_list <- paste(candidates, collapse=", ")
  demographics_list <- paste(demographics, collapse=", ")
  ei_formula <- paste('cbind(', candidates_list, ') ~ cbind(', demographics_list, ')', sep='')
  tune.nocov <- tuneMD(ei_formula,
                       data = data,
                       ntunes = ntunes_val,
                       totaldraws = tunedraws)

  md.out <- ei.MD.bayes(ei_formula,
                        covariate = NULL, # what does this do?
                        data = data,
                        sample = sample_mcmc,
                        thin = thin_mcmc,
                        burnin=burnin_mcmc,
                        ret.mcmc=TRUE,
                        tune.list = tune.nocov)

  df_alpha <- data.frame(as.matrix(md.out$draws$Alpha))
  df_beta <- data.frame(as.matrix(md.out$draws$Beta))
  df_counts <- data.frame(as.matrix(md.out$draws$Cell.count))
  df_tunes_alpha <- data.frame(as.matrix(tune.nocov$tune.alpha))
  df_tunes_beta <- data.frame(as.matrix(tune.nocov$tune.beta))

  set.seed(1)
  beta_precincts <- sample(seq(1:nrow(data)), 4) # randomly choose 10 precincts to winnow betas
  precinct <- function(col) {
    l <- strsplit(col, "[.]")[[1]]
    strtoi(tail(l, n=1))
  }
  keeps <- c()
  for (col in names(df_beta)) {
    if (precinct(col) %in% beta_precincts) {
      keeps <- c(keeps, col)
    }
  }
  winnowed_df_beta <- df_beta[keeps]

  write.csv(df_alpha, paste(output_dir, "/MD_alpha.csv", sep=""), row.names=FALSE)
  write.csv(winnowed_df_beta, paste(output_dir, "/MD_beta.csv", sep=""), row.names=FALSE)
  write.csv(df_counts, paste(output_dir, "/MD_counts.csv", sep=""), row.names=FALSE)
  write.csv(df_tunes_alpha, paste(output_dir, "/MD_tunes_alpha.csv", sep=""), row.names=FALSE)
  write.csv(df_tunes_beta, paste(output_dir, "/MD_tunes_beta.csv", sep=""), row.names=FALSE)

  qq <- md.out$draws$Beta
  # print("QQ dim is:")
  # print(dim(qq))
  # write.csv(qq, paste(output_dir, "/qq.csv", sep=""))
  num_c <- length(candidates)
  num_d <- length(demographics)

  i <- 1
  for (candidate in candidates) {
    for (group in demographics) {
      proportions_col <- paste(group, candidate, "prop", sep="_")
      votes_col <- paste("EI", group, candidate, sep="_")
      product <- num_c * num_d

      data_length = dim(data)[1] # TODO: figure out why this and the below don't line up
      data_length = as.integer(dim(qq)[2] / product)
      # print(data_length) # this should equal length(data) but it doesn't...

      data[[proportions_col]] <- apply(qq[,c(product * (1:data_length)-(product-i))],2,mean)
      data[[votes_col]] <- round(data[[proportions_col]] * data[[group]])
      cols <- names(data)
      cols <- cols[!cols %in% c(proportions_col)]
      data <- subset(data, select = cols) # stripping out proportions columns
      i <- i+1
    }
  }
  cols <- names(data)
  cols <- cols[!cols %in% c("factor")]
  data <- subset(data, select = cols)

  write.table(data, paste(output_dir, "/prec_mean_counts.csv", sep=""), row.names = F, col.names = (!file.exists(paste(output_dir, "/prec_mean_counts.csv", sep=""))), append = file.exists(paste(output_dir, "/prec_mean_counts.csv", sep="")), sep=',')
}

runs <- seq(1, 4)
mclapply(runs, run_ei, args=args, mc.cores=detectCores())
