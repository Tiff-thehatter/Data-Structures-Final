USE [EERDBS-3];
GO

-- STEP 1: Apply masking ONLY to Member_Name
BEGIN TRY
    -- First check if column exists
    IF EXISTS (SELECT * FROM sys.columns 
               WHERE object_id = OBJECT_ID('dbo.Transaction_Table') 
               AND name = 'Member_Name')
    BEGIN
        -- Remove any existing masking first (if present)
        IF EXISTS (SELECT * FROM sys.masked_columns 
                   WHERE object_id = OBJECT_ID('dbo.Transaction_Table') 
                   AND name = 'Member_Name')
        BEGIN
            ALTER TABLE dbo.Transaction_Table 
            ALTER COLUMN Member_Name DROP MASKED;
        END
        
        -- Apply new masking
        ALTER TABLE dbo.Transaction_Table 
        ALTER COLUMN Member_Name ADD MASKED WITH (FUNCTION = 'partial(2, "XXXX", 0)');
        
        PRINT 'Successfully applied masking to Member_Name column';
    END
    ELSE
    BEGIN
        PRINT 'Member_Name column not found in Transaction_Table';
    END
END TRY
BEGIN CATCH
    PRINT 'Error applying Member_Name masking: ' + ERROR_MESSAGE();
END CATCH;
GO

-- STEP 2: Create test user if needed
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'MaskedUser')
BEGIN
    CREATE USER MaskedUser WITHOUT LOGIN;
    GRANT SELECT ON SCHEMA::dbo TO MaskedUser;
    PRINT 'Created MaskedUser for testing';
END
GO

-- STEP 3: Test the masking
PRINT 'Testing Member_Name masking:';
PRINT 'Before masking (as admin):';
SELECT TOP 5 
    Receipt_No,
    Member_Name AS Original_Name,
    Payment_Method,
    Total_Payment
FROM dbo.Transaction_Table;

PRINT 'After masking (as MaskedUser):';
EXECUTE AS USER = 'MaskedUser';
    SELECT TOP 5 
        Receipt_No,
        Member_Name AS Masked_Name,
        Payment_Method,
        Total_Payment
    FROM dbo.Transaction_Table;
REVERT;
GO
