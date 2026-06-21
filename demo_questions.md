# Demo Questions

These questions are intentionally varied from the local MetaMathQA corpus entries so that RAG retrieves related examples without giving an exact duplicate of the student question.

## Hard questions from the sampled MetaMathQA corpus

1. Variant of `metamathqa_000002`: A curve is described parametrically by \[(x,y) = (2 \cos t - \sin t, 40 \sin t).\] The graph of the curve can be expressed in the form \[ax^2 + bxy + cy^2 = 1.\] Find the ordered triple \((a,b,c)\).

   Answer:
   \[
   \sin t=\frac{y}{40},\qquad \cos t=\frac{x}{2}+\frac{y}{80}.
   \]
   Therefore,
   \[
   \left(\frac{x}{2}+\frac{y}{80}\right)^2+\left(\frac{y}{40}\right)^2=1,
   \]
   so
   \[
   (a,b,c)=\left(\frac14,\frac1{80},\frac1{1280}\right).
   \]

2. Variant of `metamathqa_000061`: The points \((0,0), (1,1), (3,1), (3,0), (4,0), (2,-2), (0,0)\) are joined in order to form a hexagon. What is the perimeter in simplest radical form?

   Answer:
   The side lengths are
   \[
   \sqrt2,\;2,\;1,\;1,\;2\sqrt2,\;2\sqrt2.
   \]
   Thus the perimeter is
   \[
   4+5\sqrt2.
   \]

## Calculator/tool-needed question

3. Verify the exact solution of \(87654321x - 12345678 = 34567890\), and compute \(x\) as a simplified fraction.

   Answer:
   \[
   87654321x=34567890+12345678=46913568,
   \]
   so
   \[
   x=\frac{46913568}{87654321}=\frac{15637856}{29218107}.
   \]

## Medium grade 10-12 questions

4. Solve the quadratic equation \(3x^2 - 10x + 3 = 0\), and explain each step.

   Answer:
   \[
   3x^2-10x+3=(3x-1)(x-3)=0.
   \]
   Therefore,
   \[
   x=\frac13 \quad \text{or} \quad x=3.
   \]

5. Given the function \(f(x)=x^2-6x+5\), find the vertex, axis of symmetry, and minimum value.

   Answer:
   \[
   f(x)=x^2-6x+5=(x-3)^2-4.
   \]
   The vertex is \((3,-4)\), the axis of symmetry is \(x=3\), and the minimum value is \(-4\).

## Additional tool-call versatility questions

6. Easy but different form: Find the derivative of \(g(x)=5x^6-4x^3+9\), and verify the symbolic result.

   Answer:
   \[
   g'(x)=30x^5-12x^2.
   \]

7. Large arithmetic: A rectangular field is \(23456\) meters long and \(78901\) meters wide. Compute the exact area in square meters.

   Answer:
   \[
   23456\cdot 78901=1850701856.
   \]
   The area is \(1,850,701,856\) square meters.

8. Multi-step problem with a large intermediate calculation: A triangle has base \(b\) and height \(54321\). The base is defined by the equation
   \[
   123456789b+9876543=555555555.
   \]
   Find the exact area of the triangle as a simplified fraction.

   Answer:
   \[
   123456789b=545679012
   \]
   so
   \[
   b=\frac{545679012}{123456789}=\frac{181893004}{41152263}.
   \]
   The area is
   \[
   \frac12\cdot b\cdot 54321
   =\frac{1646768311714}{13717421}.
   \]

## Intermediate sampled MetaMathQA questions

9. Variant of `metamathqa_000010`: A positive integer can be written as \(AB\) in base 11 and as \(BA\) in base 7. What is the value of the integer in base 10?

   Answer:
   \[
   11A+B=7B+A \Rightarrow 10A=6B \Rightarrow 5A=3B.
   \]
   The valid digit pair is \(A=3\), \(B=5\), so the integer is
   \[
   11(3)+5=38.
   \]

10. Variant of `metamathqa_000112`: The quadratic equation \(ax^2+12x+c=0\) has exactly one solution. If \(a+c=13\), and \(a<c\), find the ordered pair \((a,c)\).

    Answer:
    A quadratic has exactly one solution when its discriminant is zero:
    \[
    12^2-4ac=0 \Rightarrow ac=36.
    \]
    With \(a+c=13\) and \(a<c\), the pair is
    \[
    (a,c)=(4,9).
    \]

11. Variant of `metamathqa_000217`: In a right triangle, the two legs have lengths 5 and 12. Find the length of the third side.

    Answer:
    By the Pythagorean theorem,
    \[
    c^2=5^2+12^2=25+144=169,
    \]
    so \(c=13\).

12. Variant of `metamathqa_000249`: The first three terms of an arithmetic sequence are 4, 11, and 18. What is the value of the 25th term?

    Answer:
    The common difference is
    \[
    11-4=7.
    \]
    Therefore,
    \[
    a_{25}=4+(25-1)\cdot 7=172.
    \]

13. Variant of `metamathqa_000313`: If the sum of the squares of two positive integers is 74 and their product is 35, what is the sum of the two integers?

    Answer:
    Let the integers be \(x\) and \(y\). Since
    \[
    x^2+y^2=74,\qquad xy=35,
    \]
    we have
    \[
    (x+y)^2=x^2+y^2+2xy=74+70=144.
    \]
    Because \(x\) and \(y\) are positive,
    \[
    x+y=12.
    \]

14. Variant of `metamathqa_000350`: Determine the distance between the center of the circle defined by the equation \(x^2+y^2=6x-8y+11\) and the point \((15,1)\).

    Answer:
    Complete the square:
    \[
    x^2-6x+y^2+8y=11
    \]
    so
    \[
    (x-3)^2+(y+4)^2=36.
    \]
    The center is \((3,-4)\). Its distance to \((15,1)\) is
    \[
    \sqrt{(15-3)^2+(1+4)^2}
    =\sqrt{144+25}=13.
    \]

15. Variant of `metamathqa_000387`: Given that the quotient of two positive integers is \(\frac32\) and their product is 54, what is the value of the larger integer?

    Answer:
    Let the larger integer be \(x\) and the smaller be \(y\). Then
    \[
    \frac{x}{y}=\frac32 \Rightarrow x=\frac32y.
    \]
    Substitute into \(xy=54\):
    \[
    \frac32y^2=54 \Rightarrow y^2=36 \Rightarrow y=6.
    \]
    Thus
    \[
    x=\frac32\cdot 6=9.
    \]

16. Variant of `metamathqa_000435`: The operation \(*\) is defined for non-zero integers as \(a*b=\frac1a+\frac1b\). If \(a+b=11\) and \(ab=30\), what is the value of \(a*b\)? Express your answer as a common fraction.

    Answer:
    \[
    a*b=\frac1a+\frac1b=\frac{a+b}{ab}.
    \]
    Using \(a+b=11\) and \(ab=30\),
    \[
    a*b=\frac{11}{30}.
    \]
