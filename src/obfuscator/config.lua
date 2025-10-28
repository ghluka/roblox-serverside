return {
    LuaVersion = "LuaU";

    VarNamePrefix = "NETT_WTF_";

    NameGenerator = "Il";

    PrettyPrint = false;

    Seed = 0;

    Steps = {
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