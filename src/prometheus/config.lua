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
                MinLength = 2;
                ConcatenationType = "strcat";
                CustomFunctionType = "inline";
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