return {
    LuaVersion = "LuaU";

    VarNamePrefix = "NETT_WTF_";

    NameGenerator = "Il";

    PrettyPrint = false;

    Seed = 0;

    Steps = {
        {
            Name="SplitStrings";
            Settings = {
                MinLength = 1;
                MaxLength = 2;
            }
        },
        {
            Name="ProxifyLocals";
        },
        {
            Name = "NumbersToExpressions";
        },
        {
            Name="WrapInFunction";
        },
    }
}