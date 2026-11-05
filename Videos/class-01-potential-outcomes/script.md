# Script — Class 1: Potential outcomes, Neyman–Rubin, selection bias

Narration, beat by beat. `## <BeatId>` headings are parsed by `build_beats.py` into `beats.json`;
everything under a heading until the next one is spoken text. Lines starting with `>` are
production notes and are NOT spoken.

## B01ColdOpen

> On screen: MHE NHIS table (p. 10), built row by row. 1 = excellent, 5 = poor.

Here is a table from the American National Health Interview Survey. Almost ninety-eight thousand people were asked two questions. Did you spend a night in a hospital in the last twelve months? And how would you rate your health, from one, excellent, to five, poor? The people who went to the hospital average two point seven nine. The people who did not average two point zero seven. On this scale, higher is worse. So the hospitalised are sicker, by seven tenths of a point, with a t statistic of almost fifty-nine. Taken at face value, the data are saying something alarming. Going to the hospital makes people sick. Do you believe it?

## B02BrazilToo

> On screen: PNS 2013 bar chart, SIDRA table 5082.

Before you answer, notice that this is not an American quirk. Brazil's National Health Survey, the PNS, asked almost the same two questions in twenty thirteen. Here is what IBGE published. Among people who rated their health good or very good, four and a half percent had been hospitalised for at least twenty-four hours in the previous year. Among people who rated it regular, eight point eight percent. Among people who rated it bad or very bad, eighteen point eight percent. More than twelve million Brazilians had been hospitalised that year, and the pattern is unmistakable. The worse your health, the more likely you were to have been in a hospital.

Now look at the direction of the arrow. Nobody thinks the hospital is what put these people in poor health. It is far more natural to read the bars the other way. Poor health sends people to the hospital. The sick select themselves into treatment. And that is the whole difficulty in one picture. The thing we want to measure is the effect of the hospital on health. The thing the data are full of is the effect of health on going to the hospital. Both arrows connect the same two variables, and a simple comparison cannot tell them apart.

## B03WrongFirstAttempt

> On screen: the gap stays fixed while the sample grows and the t statistic climbs.

The first instinct of an empirical person is that this is a sample problem. Collect more data, and the truth will come out. Let us try it. Imagine the survey had one thousand respondents instead of ninety-eight thousand. The gap between the groups would be about the same, seven tenths of a point, but the t statistic would be much smaller. Now grow the sample to ten thousand, to one hundred thousand, to a million. The t statistic climbs without limit. The gap does not move.

More data makes us more certain of the number. It does nothing to the meaning of the number. A bigger sample estimates the difference between sick and healthy people with greater and greater precision, and that difference was never the causal effect of the hospital. This is the distinction between precision and identification, and it will follow us through the whole course.

Angrist and Pischke open their book with a better first move. Before any estimation, ask four questions. What is the causal relationship of interest? What experiment would ideally capture it? What is your identification strategy? And what is your mode of statistical inference? Today is about the first two. To state the causal question precisely, we need a language for things that did not happen.

## B04TwoWorlds

> On screen: one person, a fork in the road: hospital and home, two health values.

Take one person. Call her Ana. Last year Ana felt unwell and faced a choice: go to the hospital, or stay home. Draw that choice as a fork in the road.

On the hospital branch, Ana ends the year with some level of health. On the home branch, she ends it with some other level. Both branches are perfectly well defined before she chooses. Each one is a potential outcome: what her health would be if she went, and what it would be if she did not. The causal effect of the hospital, for Ana, is simply the difference between those two numbers. If the hospital branch leaves her healthier, the effect is positive.

Now the cruel part. Ana walks down exactly one branch. Suppose she goes to the hospital. Then we observe her health on that branch, and the other branch is gone. Not unknown in the way a parameter is unknown, waiting for more data. Gone. No survey, however large, can tell us how Ana's year would have gone had she stayed home, because that year never happened.

This is the idea that Donald Rubin formalised in the nineteen seventies, building on Jerzy Neyman's work on agricultural experiments in the nineteen twenties. That is why it is called the Neyman–Rubin model, or the potential outcomes framework. Its first move is exactly what we just drew. Every unit carries two outcomes, and treatment chooses which one we get to see.

## B05TheTable

> On screen: the 8-person table with Y0 and Y1 columns. Health index 0 to 10, higher is healthier.

Now give Ana seven neighbours, and give ourselves a power no researcher has. We can see both branches for everyone.

Here is the table. Eight people: Ana, Bruno, Carla, Davi, Elisa, Fábio, Gabi and Hugo. Health is measured on an index from zero to ten, and this time higher is healthier, the opposite of the American survey. The column in orange is y zero: each person's health if they do not go to the hospital. The column in blue is y one: their health if they do go.

Read the first four rows. Ana's health would be three at home and five in hospital. Bruno, two and five. Carla, four and six. Davi, three and four. These four are sick. Look at their orange column: without treatment they would end the year between two and four. Now the last four rows. Elisa, eight and eight. Fábio, nine and eight. Gabi, seven and eight. Hugo, eight and nine. These four are healthy either way.

One more column: d, the treatment indicator. It equals one if the person actually went to the hospital and zero if not. The four sick people went. The four healthy people stayed home. That is exactly the kind of self-selection the Brazilian bars showed us.

Let us fix the notation now that every symbol has something to point at. For person i, y zero i is the potential outcome without treatment, y one i is the potential outcome with treatment, and d i is the treatment actually received.

## B06FundamentalProblem

> On screen: the cells nobody can observe are greyed out, row by row.

Now take the god's-eye view away. In real data, which of these cells could we see?

Ana went to the hospital, so we see her blue cell, five. Her orange cell, three, is what would have happened at home. It did not happen. Grey it out. Bruno, same thing: we see five, his three at home disappears. Carla: we see six, her four disappears. Davi: we see four, his three disappears.

Elisa stayed home, so now it is the other way round. We see her orange cell, eight, and her blue cell disappears. Fábio: we see nine, his eight in hospital disappears. Gabi: we see seven. Hugo: we see eight.

Look at what is left. Exactly half the table. Every row has lost one of its two cells, and the lost cell is precisely the one we would need to compute that person's causal effect. Paul Holland called this the fundamental problem of causal inference. It is not a data-quality problem and it is not a sample-size problem. It is built into the definition. A causal effect compares two states of the world, and each unit only ever lives in one of them.

So individual effects are out of reach. The rest of this class is about what we can still learn, and about the conditions under which the visible half of the table tells the truth about the invisible half.

## B07SwitchingEquation

> On screen: textbook derivation, line by line. MHE equation 2.1.1.

Before we compute anything, let us write the link between what we see and the two potential outcomes as one equation. We will do it line by line.

Line one. The observed outcome, y i, equals y one i if d i equals one, and y zero i if d i equals zero. That is just the table in words: treatment picks the column.

Line two. Because d i is either zero or one, we can write the choice as a sum. y i equals d i times y one i, plus one minus d i, times y zero i. Check it: when d is one, the second term vanishes and we get y one. When d is zero, the first term vanishes and we get y zero.

Line three. Multiply out the second term. y i equals d i y one i, plus y zero i, minus d i y zero i.

Line four. Collect the two terms that carry d i. y i equals y zero i, plus the quantity y one i minus y zero i, times d i.

Test it on two rows of our table. Ana: y zero is three, the effect is two, and d is one. Three plus two times one is five, her observed health. Elisa: y zero is eight, the effect is zero, and d is zero. Eight plus zero times zero is eight. The equation reproduces every observed cell.

This is equation two point one point one in Mostly Harmless Econometrics, and it is worth reading slowly. Everyone starts from their untreated outcome, y zero i. Treatment adds that person's own causal effect, y one i minus y zero i, and only for the people with d equal to one. The effect sits inside the equation, multiplied by d. It is there in the data. We just cannot pull it out one person at a time.

## B08Estimands

> On screen: back to the full table; the effect column, then ATE, ATT, ATU computed, then named.

Go back to the god's-eye table, both columns visible, and add a third column: each person's causal effect, y one minus y zero.

Ana: five minus three, two. Bruno: five minus two, three. Carla: two. Davi: one. Elisa: eight minus eight, zero. Fábio: eight minus nine, minus one. The hospital actually makes Fábio slightly worse. Gabi: one. Hugo: one.

The effects are not all the same. That matters, so let us average them in three different ways.

Average over all eight people: two plus three plus two plus one plus zero minus one plus one plus one is nine, and nine over eight is one point one two five. Average over the four who were treated: two, three, two and one sum to eight, and eight over four is two. Average over the four who were not treated: zero, minus one, one and one sum to one, and one over four is zero point two five.

Now, and only now, the names. The first number is the average treatment effect, the ATE: the expected value of y one minus y zero over the whole population. The second is the average treatment effect on the treated, the ATT: the same expectation, conditional on d equal to one. The third is the average treatment effect on the untreated, the ATU, conditional on d equal to zero.

In this table the hospital helps the people who chose it far more than it would help the people who stayed away. That is not a coincidence. People who expect to gain from a treatment are often the ones who seek it. So the ATT and the ATE are different questions, with different answers, and any method we use has to say which one it estimates.

Which one you want depends on the decision. A health minister asking whether to keep the hospital open for the people who use it today wants the ATT. A minister asking what would happen if everyone were sent to hospital wants the ATE. And a minister thinking of extending care to people who currently stay away wants the ATU, which here is barely a quarter of a point.

## B09NaiveOnTable

> On screen: observed cells only; the two group means; the naive gap of minus three.

Now let us do what the survey did. Grey out the cells nobody can see, and compare the average health of the treated with the average health of the untreated.

The treated group: Ana five, Bruno five, Carla six, Davi four. They average five. The untreated group: Elisa eight, Fábio nine, Gabi seven, Hugo eight. They average eight.

Five minus eight. The naive comparison says that going to the hospital lowers health by three points.

Hold that next to what we know is true. The hospital raised the health of every single person who went: Ana by two, Bruno by three, Carla by two, Davi by one. The true average effect on the treated is plus two. The naive comparison is minus three. It does not merely miss the size of the effect. It gets the sign wrong.

This is the American table again, with the hidden half of the data restored. We know exactly how wrong the comparison is: five points. Where did those five points come from? The next derivation answers that, exactly.

## B10DerivationATT

> On screen: textbook derivation, numbered lines. MHE p. 11.

We start from the comparison the survey made, and we do not drop a single term.

Line one. The naive comparison is the expected outcome of the treated minus the expected outcome of the untreated. In symbols: the expectation of y i given d i equals one, minus the expectation of y i given d i equals zero.

Line two. Use the switching equation. Among the treated, the observed outcome is y one. Among the untreated, it is y zero. So line one becomes the expectation of y one i given d equals one, minus the expectation of y zero i given d equals zero.

Now the one idea in this whole derivation. These two terms describe different people and different worlds: the treated in their treated world, the untreated in their untreated world. To compare like with like, we need a bridge, a term about the treated people in the untreated world. That term is the expectation of y zero i given d equals one. We cannot observe it, but we are allowed to add it and subtract it, because adding zero changes nothing.

Line three. The expectation of y one given d equals one, minus the expectation of y zero given d equals one, plus the expectation of y zero given d equals one, minus the expectation of y zero given d equals zero.

Line four. Group the first two terms. Both condition on the treated, so by linearity of expectations they combine into the expectation of y one minus y zero, given d equals one. Group the last two terms in braces.

Line five. Name them. The first term is the average treatment effect on the treated. The bracketed term is the expected untreated outcome of the treated, minus the expected untreated outcome of the untreated. It compares the two groups in the same world, the world without hospitals. It is called selection bias.

So the observed difference in averages equals the ATT plus selection bias. Nothing was assumed. This is an identity. It holds in every dataset, for every treatment.

Read the selection-bias term once more, because it is the most important expression in this course. It does not involve treatment at all. Both terms are untreated outcomes. It asks a question about a world without hospitals: in that world, would the people who end up treated look different from the people who do not? If the answer is yes, a simple comparison is contaminated, no matter how large the sample.

## B11PlugNumbers

> On screen: the result alone, then the numbers, then a bar decomposition.

Let us put our table into this identity.

The left-hand side is the naive comparison, which we computed: minus three.

The ATT is the average effect on the four treated people: plus two.

The selection bias is the expected untreated outcome of the treated minus that of the untreated. The treated, Ana, Bruno, Carla and Davi, would have had three, two, four and three without the hospital. That averages three. The untreated, Elisa, Fábio, Gabi and Hugo, have eight, nine, seven and eight, which averages eight. Three minus eight: minus five.

Two plus minus five is minus three. The identity holds to the last decimal.

Now look at it as bars. A green bar of plus two: what the hospital does. A red bar of minus five: how much sicker the treated already were. Stack them and you get the grey bar of minus three, the number the data report. The causal effect is real and positive. It is simply buried under a selection bias more than twice its size. That is exactly what happened in the American table, and in Brazil's PNS. The people in hospital beds were not a random draw from the population. They were the sick.

## B12SignOfBias

> On screen: three cards, one at a time. MHE pp. 12–16.

Selection bias has a sign, and the sign tells you which way a naive comparison will mislead you. It depends on one question: who selects into treatment, and what would their outcomes have been anyway?

First card: job training programs. Governments run subsidised training for disadvantaged workers. Non-experimental studies often find that trainees earn less afterwards than comparable non-participants. But these programs are designed for people with low earnings potential. Their untreated earnings were already lower. Selection bias is negative, exactly like the hospital. Randomised evaluations of the same kind of programs find mostly positive effects.

Second card: hormone replacement therapy. A large observational survey of nurses found better health among women who took it. Then a randomised trial found few benefits, and serious side effects the observational data had not revealed. Here the women who chose the therapy differed from those who did not in ways that flattered it. Selection bias was positive. It made a weak treatment look good.

Third card: class size. Naive comparisons often show students in smaller classes doing worse. But schools deliberately place weaker students in smaller classes. Their untreated scores were lower. Negative selection bias again, hiding the benefit of small classes.

So there is no general rule that naive comparisons overstate or understate effects. You have to ask, for each application, who walks through the door, and why.

## B12bMirror

> On screen: the same table, but now the four healthy people are the treated. Same identity, opposite sign.

To see that the sign really comes from who selects in, keep the same eight people and the same two columns, and change only who goes to the hospital. Suppose the hospital is a private clinic offering elective check-ups, and it is the healthy who use it: Elisa, Fábio, Gabi and Hugo. The sick four stay home.

Nothing about anyone's potential outcomes has changed. Only the d column.

Now the treated show their blue cells: eight, eight, eight and nine, an average of eight and a quarter. The untreated show their orange cells: three, two, four and three, an average of three. The naive comparison is plus five and a quarter. Five points of benefit from a clinic.

Run the identity. The ATT is now the average effect on the healthy four: zero, minus one, one and one, which is one quarter. Selection bias is the untreated outcome of the treated, eight, minus the untreated outcome of the untreated, three: plus five. One quarter plus five is five and a quarter.

The same people, the same treatment, the same true effects. One way of sorting them into treatment makes the hospital look harmful by three points. The other makes it look miraculous by more than five. The data never changed their potential outcomes. Only the selection rule changed, and the selection rule is what the naive comparison actually measures.

## B13DerivationATE

> On screen: textbook derivation, numbered lines. Standard extension of MHE §2.1.

Our identity delivered the ATT. But a policy that sends everyone to the hospital is evaluated by the ATE. How far is the naive comparison from the ATE? One more derivation.

Let pi be the share of the population that is treated. In our table, pi is one half.

Line one. The ATE is an average over everyone, so it is a weighted average of the effect on the treated and the effect on the untreated. The ATE equals pi times the ATT, plus one minus pi, times the ATU. That is the law of iterated expectations.

Line two. Rewrite pi times the ATT as the ATT minus one minus pi times the ATT. Then the ATE equals the ATT, minus one minus pi times the ATT, plus one minus pi times the ATU.

Line three. Collect the two terms that share one minus pi. The ATE equals the ATT minus one minus pi, times the quantity ATT minus ATU.

Line four. Solve for the ATT. The ATT equals the ATE plus one minus pi, times ATT minus ATU.

Line five. Take our identity from before: the naive comparison equals the ATT plus selection bias. Substitute line four for the ATT.

Line six. The naive comparison equals the ATE, plus selection bias, plus one minus pi times the difference between the ATT and the ATU.

Two distinct problems now sit between the data and the ATE. The first is selection bias, which is about baseline differences: the groups differ even without treatment. The second is heterogeneous treatment effect bias: the groups would gain different amounts from treatment. If everyone had the same effect, the ATT would equal the ATU, and the second term would vanish. In our table they do not.

The sign of that second term also has a story. When people select into treatment because they expect to gain from it, the treated gain more than the untreated would, so the ATT exceeds the ATU and the term is positive. A naive comparison then leans toward the effect on the eager, not the effect on the average person.

## B14PlugATE

> On screen: the line-six identity with numbers substituted, then a bar decomposition.

Plug in the table. The ATE is one point one two five. Selection bias is minus five. Pi is one half, the ATT is two and the ATU is zero point two five, so the last term is one half times one point seven five, which is zero point eight seven five.

One point one two five, minus five, plus zero point eight seven five. That is minus three. The same number the survey would report, now split into three honest pieces: the average effect, the baseline difference, and the difference in gains.

## B15Independence

> On screen: the table with D re-drawn by coin flips; then the independence statement.

So how does an experiment escape both terms? By taking the decision away from the people.

Go back to our eight. Instead of letting the sick choose the hospital, flip a coin for each of them. Heads, hospital. Tails, home. Watch the d column change. Now the treated group might contain Ana and Elisa, Fábio and Hugo, a mixture of sick and healthy. The coin has no idea who is sick. It cannot look at the orange column, and it cannot look at the blue column.

That sentence is the whole assumption, and here is its formal version. Random assignment makes the treatment indicator independent of the potential outcomes. The pair y zero i, y one i is independent of d i.

Be careful about what this does and does not say. It does not say that treatment is unrelated to the observed outcome. If the hospital works, treated people will have better observed health. It says that treatment is unrelated to the outcomes people would have had, in either world. Who gets treated tells you nothing about anyone's y zero or y one. In the self-selected table, d equal to one told you the person was sick. After the coin, d tells you nothing at all about the person.

## B16DerivationRandom

> On screen: textbook derivation, numbered lines. MHE p. 12.

Now feed independence into our identities and watch the bias terms die. Line by line.

Line one. Selection bias is the expectation of y zero given d equals one, minus the expectation of y zero given d equals zero.

Line two. Independence means conditioning on d does not change the distribution of y zero. So both conditional expectations equal the unconditional one. Selection bias equals the expectation of y zero minus the expectation of y zero, which is zero.

Line three. The ATT is the expectation of y one given d equals one, minus the expectation of y zero given d equals one.

Line four. By the same argument applied to both potential outcomes, the conditioning drops from each term. The ATT equals the expectation of y one minus the expectation of y zero, which is the ATE.

Line five. The same steps applied to the untreated give the ATU equal to the ATE as well. So the ATT minus the ATU is zero, and the heterogeneity term vanishes too.

Line six. Put it together. Under random assignment, the naive comparison, the plain difference in average outcomes between treated and control, equals the ATE.

Angrist and Pischke summarise this in one sentence: random assignment eliminates selection bias. The effect of randomly assigned treatment on the treated is the effect on a randomly chosen person. That is why a randomised trial is the benchmark against which every other method in this course will be judged.

## B16bIdealExperiment

> On screen: the design of the ideal hospital experiment, built as a flow diagram. MHE Ch. 1 FAQ 2.

Angrist and Pischke's second question was: what experiment would ideally answer this? For the hospital, we can now write it down.

Take patients who arrive at an emergency room with symptoms for which doctors are genuinely unsure whether admission helps. For each one, flip a coin. Heads, admit. Tails, treat and send home. A year later, measure everyone's health with the same survey question. Compare the average of the admitted with the average of the sent-home.

Notice three things this design does. It restricts the population to cases where admission is plausibly optional, so the question being answered is the effect at the margin where policy actually operates. It assigns treatment by chance, so selection bias is zero. And it measures the outcome the same way in both arms.

Of course, no ethics committee would approve flipping coins over seriously ill patients. Many ideal experiments are like this: impossible, or too expensive, or too slow. But writing the ideal experiment down is still the right first step. It tells you exactly which comparison you are trying to imitate. Every method in the rest of this course, from controls and fixed effects to instrumental variables, differences in differences and regression discontinuity, can be understood as an attempt to approximate this coin flip with data nobody randomised.

## B17CoinFlips

> On screen: one coin-flip draw (Ana, Elisa, Fábio, Hugo treated) giving 3.5; then the histogram of all 70 assignments.

Notice that every line of that derivation was about expectations. Let us see what that means on our actual eight people.

Flip the coins once. Suppose four people come up heads: Ana, Elisa, Fábio and Hugo. Their observed health in hospital is five, eight, eight and nine, which averages seven and a half. The other four, Bruno, Carla, Davi and Gabi, stay home with two, four, three and seven, which averages four. The difference in means is three and a half. The true ATE is one point one two five. One experiment, and it is off by more than two points.

Did randomisation fail? No. Let us run every possible experiment. With eight people and four treated, there are seventy ways to choose the treated group. Here is the difference in means for each of the seventy. Some experiments say minus three. Some say plus five and a quarter. They scatter widely. But their average, the vertical line, sits at exactly one point one two five, the ATE, to every decimal place.

That is what unbiased means. Randomisation removes the systematic error. It does not remove chance. With eight people, chance is large. With eleven thousand children, as in the experiment we are about to see, chance becomes small. So sample size matters after all, but only after randomisation has made the comparison about the right thing.

## B17bSampleSize

> On screen: four histograms of the difference in means, for 8, 80, 800 and 8,000 people. Same centre, shrinking spread.

How fast does chance shrink? Let us measure it. Take our eight people and imagine a population made of ten copies of them, then a hundred copies, then a thousand. In each case, randomly treat half and compute the difference in means, many thousands of times.

With eight people, the estimates scatter with a standard deviation of about one point six. With eighty people, about zero point four eight. With eight hundred, about zero point one five. With eight thousand, about zero point zero five. Every one of these distributions is centred on the same number, one point one two five.

Two lessons sit in this picture. First, the spread falls with the square root of the sample size. Multiply the sample by one hundred, and the spread falls by a factor of ten. Second, compare this with the picture from the start of the class. There, a bigger sample made us more and more confident about a biased number. Here, a bigger sample makes us more and more confident about the right number. Sample size is worth having only once the design has made the comparison unbiased. Identification first, precision second.

## B18SUTVA

> On screen: two rows connected by an arrow (interference); then the two parts of the assumption.

The table itself rests on an assumption we have been using silently. When we wrote two potential outcomes per person, we assumed that each person's outcome depends only on their own treatment.

Suppose instead that hospitalised patients bring an infection home. Then Elisa's health at home depends on whether her husband went to the hospital. Her y zero is no longer one number. It changes with other people's d. With eight people and two treatments each, there are two hundred and fifty-six ways to assign treatment, and Elisa could have a different outcome under every one of them. Our two-column table stops making sense.

Rubin called the condition that rules this out the stable unit treatment value assumption, SUTVA. It has two parts. First, no interference: one person's treatment does not change another person's potential outcomes. Second, no hidden versions of treatment: going to the hospital means the same thing for everyone who goes.

SUTVA is not tested by the data. It is a judgement about the setting. Vaccines, classrooms where students learn from each other, markets where one firm's subsidy moves another firm's price: these are all places where it can fail, and where the Neyman–Rubin table has to be redrawn.

## B19STARBalance

> On screen: MHE Table 2.2.1 (adapted from Krueger 1999), built row by row. MHE pp. 13–14.

Now a real experiment. In the mid-nineteen eighties, the state of Tennessee spent about twelve million dollars on Project STAR. About eleven thousand six hundred children, starting in the nineteen eighty-five kindergarten cohort, were randomly assigned within their schools to one of three class types: small classes of thirteen to seventeen children, regular classes of twenty-two to twenty-five with a part-time teacher's aide, or regular classes with a full-time aide.

The first question to ask of any experiment is whether randomisation worked. If it did, the groups should look alike on everything determined before treatment. Here is the check, from Krueger's analysis.

The share of children receiving a free lunch, a good proxy for family income: forty-seven percent in small classes, forty-eight in regular, fifty in regular with aide. The share white or Asian: sixty-eight, sixty-seven, sixty-six. Age in nineteen eighty-five: five point four four, five point four three, five point four two years. None of these differences is statistically significant. The groups are balanced, as the coin promised. One row does differ: attrition, the share of children lost before third grade, was lower in small classes. Krueger examines that problem in detail, and it is why the kindergarten results are the most reliable.

Then the rows that should differ. Class size: fifteen point one in small classes, against twenty-two point four and twenty-two point eight. The experiment really did create the variation it was designed to create. And the kindergarten percentile score: fifty-four point seven in small classes, against forty-eight point nine and fifty.

## B20STAREffect

> On screen: MHE Table 2.2.2 (adapted from Krueger 1999, Table 5), columns (1)–(4). MHE p. 15.

Because assignment was random, the difference in average scores between small and regular classes estimates the causal effect of class size. Krueger computes it as a regression of test scores on dummies for each treatment group. Here are the estimates.

Column one, no controls at all: small classes raise the percentile score by four point eight two points, with a standard error of two point one nine. Column two adds school fixed effects, because randomisation happened within schools: five point three seven, standard error one point two six. Column three adds the children's own characteristics, race, sex and free lunch status: five point three six, standard error one point two one. Column four adds teacher characteristics: five point three seven, standard error one point one nine.

Watch the two rows move differently. The estimate barely changes, from about four point eight to about five point four, and then not at all. That is what balance buys you. The controls are unrelated to treatment, so they cannot remove a bias that randomisation already removed. But the standard error falls from two point one nine to one point one nine, because the controls explain a large part of why children's scores differ. They make the estimate more precise without changing what it estimates.

The result is a small-class effect of about five percentile points, roughly one fifth of a standard deviation. The regular-with-aide classes, by contrast, show an effect that is small and not significant.

## B21RegressionForm

> On screen: textbook derivation, numbered lines. MHE equation 2.3.1, pp. 16–17.

Krueger used a regression, so let us close the loop between regression and potential outcomes. Again, line by line.

Line one. Start from the switching equation. y i equals y zero i plus y one i minus y zero i, times d i.

Line two. Suppose, for now, that the effect is the same for everyone: y one i minus y zero i equals a constant, rho. Then y i equals y zero i plus rho d i.

Line three. Split the untreated outcome into its mean and a deviation. y zero i equals alpha plus eta i, where alpha is the expected value of y zero and eta i is the random part.

Line four. Substitute. y i equals alpha plus rho d i plus eta i. This is equation two point three point one: a regression of the outcome on the treatment dummy.

Line five. Take expectations with d switched on and off. The difference in conditional means equals rho, plus the expectation of eta given d equals one, minus the expectation of eta given d equals zero.

Line six. Since eta is just y zero minus a constant, that last bracket is exactly our selection bias: the expected y zero of the treated minus that of the untreated.

So selection bias, in regression language, is correlation between the regressor and the error term. The sick have low eta, and the sick are the ones with d equal to one. Random assignment breaks that correlation, and the regression coefficient on d recovers rho.

## B21bRecap

> On screen: four numbered skills, one at a time.

Before the closing picture, here is what you should now be able to do on your own.

One. Given a causal question, write down the two potential outcomes, the treatment indicator, and the switching equation that links them to the data. Say in words what y zero and y one mean for the problem at hand.

Two. Define the ATE, the ATT and the ATU, compute them from a table where both potential outcomes are known, and say which one a given policy question needs.

Three. Derive, line by line, that the naive difference in means equals the ATT plus selection bias, and that it equals the ATE plus selection bias plus the heterogeneity term. Then sign the selection bias in an application by asking who selects into treatment and what their untreated outcomes would have been.

Four. Show that random assignment makes selection bias and the heterogeneity term vanish in expectation, explain why one small experiment can still miss, and list what randomisation does not solve: the stable unit treatment value assumption, attrition, and the precision that only sample size provides.

If any of these four feels shaky, rewatch the derivation that goes with it. Each one is a line-by-line argument you should be able to reproduce with a pencil.

## B22Closing

> On screen: the closing image. Hold.

Here is the picture to keep.

Eight rows, two potential outcomes each, and half the cells grey forever. That is the fundamental problem: every causal effect compares two worlds, and every person lives in one.

Underneath, the one line that holds in every dataset: the observed gap equals the effect on the treated, plus selection bias. And on the selection bias, a coin. When treatment is assigned by chance rather than by choice, that term disappears, and the simple difference in means tells the truth about the average effect.

Next class, we ask what to do when there is no coin, and whether controlling for the right variables can stand in for one.
