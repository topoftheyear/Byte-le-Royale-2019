db.getCollection('users').updateMany(
    // query 
    {
       
    },
    
    // update 
    {
        "$set": {"submissions.$[].runs": []}
    },
    
    // options 
    {

    }
);