<?php namespace nm;

$a = 1;

$GLOBALS['_'] = 2;

define('op', 'op');
const op2 = 2;

function fucn()
{
	echo $GLOBALS['a'];

	while ($GLOBALS['a'] != 1)
	{
			$GLOBALS['a']++;
	}
	$GLOBALS['b'] = 6;
}

/**
 * MyClass title
 *
 * MyClass
 * description
 *
 * @package none
 * @author Andrii Perun
 * @version 1.3
 */
class MyClass
{
    const CONSTANT = 'const value';
		/**
		* @var string $var1 Description for var1
		*/
    public $var1;
		/**
		* @var string $var2 Description for var2
		*/
    protected $var2;
		/**
		* @var string $var3
		*/
    private $var3;

    function __construct()
		{
       print "MyClass constructor\n";
       print op;
    }

    function __destruct()
    {
       print "Delete " . __CLASS__  . "\n";
    }
		/**
		* Simple method title
		* Simple method description
		*
		* @return string
		* @param string $param3
		* @param string $param1
		*/
    function method($param1, $param2)
    {
			return $param1 + $param2;
    }
}

class MyClass2 extends MyClass
{
	protected $var = 2;
}

$obj = new MyClass2();

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

		private $var_a = 1;
		protected $var_b = 2;
		public $var_c = 3;


		protected function useA()
		{
				for ($i = 0; $i < 10; $i++)
					for ($j = 0; $j < 10; $j++)
					{
						for ($y = 0; $y < 10; $y++)
						{
							echo a;
						}
					}
		}

		private function useB()
		{
			for ($i = 0; $i < 10; $i++)
				for ($j = 0; $j < 10; $j++)
				{
					for ($y = 0; $y < 10; $y++)
					{
						echo b;
					}
				}
		}
}

?>
