<?php
/**
* Title
* description
* @author Andrii Perun <andrewfreelan@gmail.com>
*/

/**
 * MyClass title
 *
 * MyClass
 * description
 *
 * @package none
 * @author Andrii Perun
 * @version 1.3
 * @access public
 * @see reference/to/class
 */
class MyClass
{
    const CONSTANT = 'stirng';
    public $var1;
    protected $var2;
    private $var3;

    function __construct()
    {
       print "MyClass constructor\n";
    }

    function __destruct()
    {
       print "Delete " . __CLASS__  . "\n";
    }

    function method($var1, $varn)
    {
    }
}
$GLOBALS['p'] = 5;
$var = 4;
const c = 'fdf';
/**
 * Title
 */
interface InterfaceName
{
	public const a = 5;
	public function method1($var1, $_varvar1_1);
}

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

/**
* title
* description
* @param int $var var description
* @return string
*/
function func($var)
{
  echo $var + 1;
  echo $var + 2;
  echo $var + 3;
}

/**
* title
* description
* @param int $var var description
* @return string
*/
function func2($var)
{
  echo $var + 4;
  echo $var + 5;
  echo $var + 6;
}


?>
