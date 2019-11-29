<?php
/**
* Title
* description
* @version 1.5
* @author Andrii Perun <andrewfreelan@gmail.com>
*/

/**
*
*/
namespace nm;
$GLOBALS['a'] = 5;
$b = 4;
const c = 'fdf';
function func2($var)
{
  echo $var;
}

namespace nm\mn;
/**
* title
* description
* @param int $var var description
* @return string
*/
function fun3c($var)
{
  echo $var + 1;
  include 'f3.php';
  class MyClass {
      //include 'f3.php';
      public $public = 'Public';
  }

  $var2 =  new MyClass();

}

define('myconst', 2);

trait Hello
{
    public function sayHello()
		{
        echo 'Hello ';
    }
		private $a;

		protected function useA()
		{
				for ($i = 0; $i < 10; $i++)
					for ($j = 0; $j < 10; $j++)
					{
						for ($y = 0; $y < 10; $y++)
						{
							echo $a;
						}
					}
		}
}
const c = 'fdf2';
namespace nm;

echo mn\c;
namespace nm\mn;
echo c;
fun3c(4);

?>
