<?php namespace ns;
  $var1 = 7;
  function f_($var)
  {
      echo $var;
  }
  $a = 1;
  $GLOBALS['_'] = 2;
  define('op', 'op');
  const op2 = 2;
  function fucn()
  {
  	echo $GLOBALS['a'];
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
   * @access public
   * @see reference/to/class
   */
  class MyClass
  {
      const CONSTANT = '�������� ���������';
      public $var1;
      protected $var2;
      private $var3;
      function __construct() {
         print "MyClass constructor\n";
         print op;
      }
      function __destruct()
      {
         print "Delete " . __CLASS__  . "\n";
      }
      function method()
      {
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
  }
?>
