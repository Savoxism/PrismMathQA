# Demo Questions

## Hard questions from the sampled MetaMathQA corpus

1. `metamathqa_000002`: A curve is described parametrically by \[(x,y) = (2 \cos t - \sin t, X \sin t).\] The graph of the curve can be expressed in the form \[ax^2 + bxy + cy^2 = 1.\] Enter the ordered triple \((a,b,c)\). If \(X=64\), find the triple.

   Answer:
   \[
   (a,b,c)=\left(\frac14,\frac{1}{128},\frac{5}{16384}\right).
   \]

2. `metamathqa_000061`: The points \((0,1), (1,2), (2,2), (2,1), (3,1), (2,0), (0,1)\) are joined in order to form a hexagon. The perimeter of the hexagon can be expressed as \(a+b\sqrt{2}+c\sqrt{5}\), where \(a,b,c\) are integers. What is \(a+b+c\)?

   Answer:
   \[
   3+2\sqrt2+\sqrt5
   \]
   so \(a=3\), \(b=2\), \(c=1\), and
   \[
   a+b+c=6.
   \]

## Calculator/tool-needed question

3. Verify the exact solution of \(987654321x - 123456789 = 555555555\), and compute \(x\) as a simplified fraction.

   Answer:
   \[
   987654321x=555555555+123456789=679012344
   \]
   so
   \[
   x=\frac{679012344}{987654321}.
   \]
   Since \(\gcd(679012344,987654321)=9\),
   \[
   x=\frac{75445816}{109739369}.
   \]

## Medium grade 10-12 questions

4. Solve the quadratic equation \(2x^2 - 7x + 3 = 0\), and explain each step.

   Answer:
   \[
   2x^2-7x+3=(2x-1)(x-3)=0.
   \]
   Therefore,
   \[
   x=\frac12 \quad \text{or} \quad x=3.
   \]

5. Given the function \(f(x)=x^2-4x+1\), find the vertex, axis of symmetry, and minimum value.

   Answer:
   \[
   f(x)=x^2-4x+1=(x-2)^2-3.
   \]
   The vertex is \((2,-3)\), the axis of symmetry is \(x=2\), and the minimum value is \(-3\).

## Additional tool-call versatility questions

6. Easy but different form: Find the derivative of \(g(x)=7x^5-3x^2+11\), and verify the symbolic result.

   Answer:
   \[
   g'(x)=35x^4-6x.
   \]

7. Large arithmetic: A rectangular field is \(123456\) meters long and \(789012\) meters wide. Compute the exact area in square meters.

   Answer:
   \[
   123456\cdot 789012=97408265472.
   \]
   The area is \(97,408,265,472\) square meters.

8. Multi-step problem with a large intermediate calculation: A triangle has base \(b\) and height \(123456\). The base is defined by the equation
   \[
   246813579b+135792468=987654321.
   \]
   Find the exact area of the triangle as a simplified fraction.

   Answer:
   \[
   246813579b=851861853
   \]
   so
   \[
   b=\frac{851861853}{246813579}=\frac{94651317}{27423731}.
   \]
   The area is
   \[
   \frac12\cdot b\cdot 123456
   =\frac12\cdot \frac{94651317}{27423731}\cdot 123456
   =\frac{5842636495776}{27423731}.
   \]
