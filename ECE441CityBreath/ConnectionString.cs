using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ECE441CityBreath
{
    class DBUtils
    {
        public static String GetDBConnection()
        {
            String var = "Server=104.194.104.247;Database=Gas;port=3306;User Id=Admin;password=I6xH#w92K;";
            return var;
        }
    }
}
